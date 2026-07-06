import numpy as np
from gnuradio import gr


class blk(gr.basic_block):
    """
    Sincronizador MPEG-TS robusto por bits.

    Entrada:
        Bits uint8 desde GMSK Demod.

    Salida:
        Bytes uint8 alineados en paquetes MPEG-TS de 188 bytes.
    """

    def __init__(self,
                 packet_len=188,
                 sync_byte=0x47,
                 lock_window=9,
                 lock_threshold=8,
                 unlock_after=20,
                 max_buffer_bits=500000,
                 debug=True):

        gr.basic_block.__init__(
            self,
            name="mpegts_bit_sync_robust",
            in_sig=[np.uint8],
            out_sig=[np.uint8],
        )

        self.packet_len = int(packet_len)
        self.sync_byte = int(sync_byte) & 0xFF
        self.lock_window = int(lock_window)
        self.lock_threshold = int(lock_threshold)
        self.unlock_after = int(unlock_after)
        self.max_buffer_bits = int(max_buffer_bits)
        self.debug = bool(debug)

        self.packet_bits = self.packet_len * 8
        self.bits = []
        self.locked = False
        self.bad_packets = 0

        self.set_output_multiple(self.packet_len)

    def _byte_at(self, bit_pos):
        if bit_pos + 8 > len(self.bits):
            return None

        value = 0

        for b in self.bits[bit_pos:bit_pos + 8]:
            value = (value << 1) | (int(b) & 1)

        return value & 0xFF

    def _packet_to_bytes(self, start_bit):
        pkt = bytearray(self.packet_len)

        for i in range(self.packet_len):
            b = self._byte_at(start_bit + i * 8)

            if b is None:
                return None

            pkt[i] = b

        return bytes(pkt)

    def _find_sync(self):
        required_bits = (self.lock_window - 1) * self.packet_bits + 8

        if len(self.bits) < required_bits:
            return False

        last_start = len(self.bits) - required_bits + 1

        for start in range(last_start):

            if self._byte_at(start) != self.sync_byte:
                continue

            hits = 1

            for k in range(1, self.lock_window):
                pos = start + k * self.packet_bits

                if self._byte_at(pos) == self.sync_byte:
                    hits += 1

            if hits >= self.lock_threshold:

                if start > 0:
                    del self.bits[:start]

                self.locked = True
                self.bad_packets = 0

                if self.debug:
                    print(
                        f"[mpegts_bit_sync] LOCK start={start}, "
                        f"hits={hits}/{self.lock_window}"
                    )

                return True

        if len(self.bits) > self.max_buffer_bits:
            keep = required_bits + self.packet_bits
            self.bits = self.bits[-keep:]

        return False

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        if len(inp) > 0:
            self.bits.extend((inp & 1).astype(np.uint8).tolist())

        self.consume(0, len(inp))

        produced = 0

        if not self.locked:
            self._find_sync()
            return 0

        while len(self.bits) >= self.packet_bits and produced + self.packet_len <= len(out):

            sync = self._byte_at(0)

            if sync == self.sync_byte:
                pkt = self._packet_to_bytes(0)

                if pkt is None:
                    break

                out[produced:produced + self.packet_len] = np.frombuffer(
                    pkt, dtype=np.uint8
                )

                produced += self.packet_len

                del self.bits[:self.packet_bits]
                self.bad_packets = 0

            else:
                # Antes de descartar un paquete completo, buscar si el 0x47
                # está corrido algunos bits hacia adelante.
                shift_found = None

                for shift in range(1, 8):
                    if self._byte_at(shift) == self.sync_byte:
                        shift_found = shift
                        break

                if shift_found is not None:
                    if self.debug:
                        print(
                            f"[mpegts_bit_sync] BIT REALIGN shift={shift_found}, "
                            f"old_sync=0x{sync:02X}"
                        )

                    del self.bits[:shift_found]
                    self.bad_packets = 0
                    continue

                # Si no hay realineación local posible, recién ahí se descarta el paquete.
                self.bad_packets += 1

                if self.debug:
                    print(
                        f"[mpegts_bit_sync] BAD packet sync=0x{sync:02X}, "
                        f"bad={self.bad_packets}/{self.unlock_after}"
                    )

                del self.bits[:self.packet_bits]

                if self.bad_packets >= self.unlock_after:
                    if self.debug:
                        print("[mpegts_bit_sync] LOST LOCK")

                    self.locked = False
                    self.bad_packets = 0
                    self._find_sync()

                    if not self.locked:
                        break

        return produced