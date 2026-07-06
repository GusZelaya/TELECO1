import socket
import time
from collections import deque

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):
    """
    Fuente MPEG-TS continua para GNU Radio.

    - Escucha paquetes MPEG-TS por UDP.
    - Reordena a paquetes de 188 bytes.
    - Si no hay video disponible, emite paquetes nulos MPEG-TS.
    - Evita que el modulador GMSK se quede sin datos.
    """

    def __init__(self, in_port=4999, packet_len=188,
                 max_queue_packets=500, debug=False):

        gr.sync_block.__init__(
            self,
            name="mpegts_udp_pacer_source",
            in_sig=[],
            out_sig=[np.uint8],
        )

        self.in_port = int(in_port)
        self.packet_len = int(packet_len)
        self.max_queue_packets = int(max_queue_packets)
        self.debug = bool(debug)

        # Generador pseudoaleatorio para el payload de paquetes nulos.
        self.lfsr = 0xACE1

        self.queue = deque()
        self.rxbuf = bytearray()

        self.sent_video = 0
        self.sent_null = 0
        self.dropped = 0
        self.last_print = time.monotonic()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 * 1024 * 1024)
        except Exception:
            pass

        self.sock.bind(("127.0.0.1", self.in_port))
        self.sock.setblocking(False)

        self.set_output_multiple(self.packet_len)

        if self.debug:
            print(f"[mpegts_udp_pacer_source] Escuchando UDP {self.in_port}")

    def _pn_byte(self):
        """
        Genera un byte pseudoaleatorio mediante LFSR de 16 bits.
        Se usa solamente para rellenar el payload de paquetes nulos MPEG-TS.
        """

        out = 0

        for _ in range(8):
            newbit = (
                ((self.lfsr >> 0) ^
                 (self.lfsr >> 2) ^
                 (self.lfsr >> 3) ^
                 (self.lfsr >> 5)) & 1
            )

            self.lfsr = ((self.lfsr >> 1) | (newbit << 15)) & 0xFFFF
            out = (out << 1) | (self.lfsr & 1)

        return out & 0xFF

    def _make_null_packet(self):
        """
        Genera un paquete nulo MPEG-TS válido.

        Header:
            0x47       sync byte
            0x1F 0xFF  PID = 0x1FFF, paquete nulo
            0x10       payload only
        """

        payload = bytes(self._pn_byte() for _ in range(self.packet_len - 4))
        return bytes([0x47, 0x1F, 0xFF, 0x10]) + payload

    def _drain_udp(self):
        """
        Lee todos los datagramas UDP disponibles sin bloquear.
        Extrae paquetes MPEG-TS de 188 bytes alineados con 0x47.
        """

        for _ in range(100):
            try:
                data, _addr = self.sock.recvfrom(65536)
            except BlockingIOError:
                break

            if not data:
                break

            self.rxbuf.extend(data)

            while len(self.rxbuf) >= self.packet_len:

                if self.rxbuf[0] != 0x47:
                    pos = self.rxbuf.find(b"\x47")

                    if pos < 0:
                        self.rxbuf.clear()
                        break

                    del self.rxbuf[:pos]

                if len(self.rxbuf) < self.packet_len:
                    break

                pkt = bytes(self.rxbuf[:self.packet_len])
                del self.rxbuf[:self.packet_len]

                if pkt[0] == 0x47:
                    self.queue.append(pkt)

                    if len(self.queue) > self.max_queue_packets:
                        self.queue.popleft()
                        self.dropped += 1

    def work(self, input_items, output_items):
        out = output_items[0]

        self._drain_udp()

        n_packets = len(out) // self.packet_len

        if n_packets <= 0:
            return 0

        produced = 0

        for _ in range(n_packets):

            if self.queue:
                pkt = self.queue.popleft()
                self.sent_video += 1
            else:
                pkt = self._make_null_packet()
                self.sent_null += 1

            out[produced:produced + self.packet_len] = np.frombuffer(
                pkt, dtype=np.uint8
            )

            produced += self.packet_len

        if self.debug:
            now = time.monotonic()

            if now - self.last_print >= 1.0:
                print(
                    f"[mpegts_udp_pacer_source] queue={len(self.queue):4d} "
                    f"video={self.sent_video:5d} "
                    f"null={self.sent_null:5d} "
                    f"dropped={self.dropped:4d}"
                )

                self.sent_video = 0
                self.sent_null = 0
                self.dropped = 0
                self.last_print = now

        return produced