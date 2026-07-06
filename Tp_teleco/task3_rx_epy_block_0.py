import numpy as np
from gnuradio import gr
from collections import deque

class blk(gr.basic_block):
    """
    Buffer y resincronizador simple para paquetes MPEG-TS.

    Entrada:
        Stream de bytes desde Pack K Bits.

    Salida:
        Stream de bytes hacia UDP Sink.

    Función:
        - Busca paquetes MPEG-TS de 188 bytes.
        - Acepta solamente paquetes cuyo primer byte sea 0x47.
        - Acumula una cantidad mínima antes de entregar.
        - Introduce retardo, pero mejora la estabilidad de entrega.
    """

    def __init__(self, packet_len=188, preload_packets=30):
        gr.basic_block.__init__(
            self,
            name="ts_buffer_resync",
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )

        self.packet_len = int(packet_len)
        self.preload_packets = int(preload_packets)

        self.rx_buffer = bytearray()
        self.packet_queue = deque()

        self.started = False

        self.rx_count = 0
        self.valid_count = 0
        self.drop_count = 0

        self.set_output_multiple(self.packet_len)

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        # Consumir todos los bytes disponibles de entrada
        if len(inp) > 0:
            self.rx_buffer.extend(bytes(inp))
            self.rx_count += len(inp)
            self.consume(0, len(inp))

        # Buscar paquetes MPEG-TS alineados por 0x47
        while len(self.rx_buffer) >= self.packet_len:
            # Si el primer byte es 0x47, tomamos el paquete completo
            if self.rx_buffer[0] == 0x47:
                pkt = bytes(self.rx_buffer[:self.packet_len])
                del self.rx_buffer[:self.packet_len]

                self.packet_queue.append(pkt)
                self.valid_count += 1

            else:
                # Buscar el próximo posible sync byte 0x47
                try:
                    idx = self.rx_buffer.index(0x47, 1)
                    del self.rx_buffer[:idx]
                    self.drop_count += idx
                except ValueError:
                    # Si no hay 0x47, descartamos casi todo y dejamos cola mínima
                    keep = min(len(self.rx_buffer), self.packet_len - 1)
                    self.drop_count += len(self.rx_buffer) - keep
                    self.rx_buffer = self.rx_buffer[-keep:]
                    break

        # Esperar hasta tener un buffer inicial
        if not self.started:
            if len(self.packet_queue) >= self.preload_packets:
                self.started = True
            else:
                return 0

        # Entregar paquetes completos de 188 bytes
        max_packets_out = len(out) // self.packet_len
        packets_to_send = min(max_packets_out, len(self.packet_queue))

        if packets_to_send == 0:
            self.started = False
            return 0

        pos = 0
        for _ in range(packets_to_send):
            pkt = self.packet_queue.popleft()
            out[pos:pos + self.packet_len] = np.frombuffer(pkt, dtype=np.uint8)
            pos += self.packet_len

        return pos