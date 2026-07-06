import numpy as np
from gnuradio import gr


class blk(gr.basic_block):
    """
    Modulador rectangular M-QAM.

    Entrada:
        Bytes uint8.

    Salida:
        Símbolos complejos M-QAM normalizados.

    Valores admitidos:
        M = 8, 16, 32, 64, 128, 256.
    """

    def __init__(self, M_qam=16):
        gr.basic_block.__init__(
            self,
            name="qam_mapper_rect",
            in_sig=[np.uint8],
            out_sig=[np.complex64],
        )

        self.bit_buffer = []
        self.set_M_qam(M_qam)
        self._last_M_qam = self.M_qam

    def set_M_qam(self, M_qam):
        M_qam = int(M_qam)

        print(f"[qam_mapper_rect] M_qam recibido = {M_qam}", flush=True)

        if M_qam not in [8, 16, 32, 64, 128, 256]:
            M_qam = 16

        self.M_qam = M_qam
        self.k = int(np.log2(self.M_qam))

        # QAM rectangular:
        # 8-QAM   = 4 x 2
        # 16-QAM  = 4 x 4
        # 32-QAM  = 8 x 4
        # 64-QAM  = 8 x 8
        # 128-QAM = 16 x 8
        # 256-QAM = 16 x 16
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

        self.constellation = np.zeros(self.M_qam, dtype=np.complex64)

        for idx in range(self.M_qam):
            i_idx = idx % self.i_levels
            q_idx = idx // self.i_levels

            i_val = self.i_values[i_idx]
            q_val = self.q_values[q_idx]

            self.constellation[idx] = (i_val + 1j * q_val) / self.norm

        # Al cambiar M se limpia el buffer para evitar mezclar grupos de bits.
        self.bit_buffer = []

    def _byte_to_bits(self, value):
        return [(int(value) >> i) & 1 for i in range(7, -1, -1)]

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        # Detección de cambio dinámico desde el QT GUI Chooser.
        if int(self.M_qam) != int(self._last_M_qam):
            self.set_M_qam(self.M_qam)
            self._last_M_qam = self.M_qam

            print(
                f"[qam_mapper_rect] cambio dinámico a M_qam = {self.M_qam}",
                flush=True
            )

        if len(inp) > 0:
            for byte in inp:
                self.bit_buffer.extend(self._byte_to_bits(byte))

        self.consume(0, len(inp))

        produced = 0

        while len(self.bit_buffer) >= self.k and produced < len(out):
            symbol_bits = self.bit_buffer[:self.k]
            del self.bit_buffer[:self.k]

            idx = 0

            for bit in symbol_bits:
                idx = (idx << 1) | int(bit)

            out[produced] = self.constellation[idx]
            produced += 1

        return produced