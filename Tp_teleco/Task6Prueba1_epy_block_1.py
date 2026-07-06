import numpy as np
from gnuradio import gr


class blk(gr.basic_block):
    """
    Demodulador rectangular M-QAM.

    Entrada:
        Símbolos complejos recibidos.

    Salida:
        Bytes uint8 reconstruidos.

    Valores admitidos:
        M = 8, 16, 32, 64, 128, 256.
    """

    def __init__(self, M_qam=16):
        gr.basic_block.__init__(
            self,
            name="qam_demapper_rect",
            in_sig=[np.complex64],
            out_sig=[np.uint8],
        )

        self.bit_buffer = []
        self.set_M_qam(M_qam)
        self._last_M_qam = self.M_qam

    def set_M_qam(self, M_qam):
        M_qam = int(M_qam)

        print(f"[qam_demapper_rect] M_qam recibido = {M_qam}", flush=True)

        if M_qam not in [8, 16, 32, 64, 128, 256]:
            M_qam = 16

        self.M_qam = M_qam
        self.k = int(np.log2(self.M_qam))

        self.i_bits = (self.k + 1) // 2
        self.q_bits = self.k // 2

        self.i_levels = 1 << self.i_bits
        self.q_levels = 1 << self.q_bits

        self.i_values = np.arange(
            -(self.i_levels - 1),
            self.i_levels,
            2,
            dtype=np.float32
        )

        self.q_values = np.arange(
            -(self.q_levels - 1),
            self.q_levels,
            2,
            dtype=np.float32
        )

        avg_power = (
            (self.i_levels ** 2 - 1) / 3.0 +
            (self.q_levels ** 2 - 1) / 3.0
        )

        self.norm = np.float32(np.sqrt(avg_power))

        # Al cambiar M se limpia el buffer para no mezclar símbolos viejos.
        self.bit_buffer = []

    def _nearest_index(self, value, levels):
        distances = np.abs(levels - value)
        return int(np.argmin(distances))

    def _index_to_bits(self, idx):
        return [(idx >> i) & 1 for i in range(self.k - 1, -1, -1)]

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        # Detección de cambio dinámico desde el QT GUI Chooser.
        if int(self.M_qam) != int(self._last_M_qam):
            self.set_M_qam(self.M_qam)
            self._last_M_qam = self.M_qam

            print(
                f"[qam_demapper_rect] cambio dinámico a M_qam = {self.M_qam}",
                flush=True
            )

        if len(inp) > 0:
            for sym in inp:
                i_rx = float(np.real(sym) * self.norm)
                q_rx = float(np.imag(sym) * self.norm)

                i_idx = self._nearest_index(i_rx, self.i_values)
                q_idx = self._nearest_index(q_rx, self.q_values)

                idx = q_idx * self.i_levels + i_idx

                self.bit_buffer.extend(self._index_to_bits(idx))

        self.consume(0, len(inp))

        produced = 0

        while len(self.bit_buffer) >= 8 and produced < len(out):
            byte_bits = self.bit_buffer[:8]
            del self.bit_buffer[:8]

            value = 0

            for bit in byte_bits:
                value = (value << 1) | int(bit)

            out[produced] = value
            produced += 1

        return produced