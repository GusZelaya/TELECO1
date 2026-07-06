import numpy as np
from gnuradio import gr

class blk(gr.basic_block):
    """
    Bloque de resincronización MPEG-TS.
    Entrada: flujo de bytes posiblemente desalineado.
    Salida: paquetes MPEG-TS alineados de 188 bytes.
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name="ts_resync_188",
            in_sig=[np.uint8],
            out_sig=[np.uint8],
        )

        self.packet_size = 188
        self.buffer = bytearray()

    def find_sync_position(self):
        """
        Busca una posición donde aparezcan dos bytes de sincronismo MPEG-TS
        separados exactamente 188 bytes.
        """
        ps = self.packet_size
        n = len(self.buffer)

        for i in range(max(0, n - 2 * ps)):
            if self.buffer[i] == 0x47 and self.buffer[i + ps] == 0x47:
                return i

        return -1

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        if len(inp) > 0:
            self.buffer.extend(inp.tobytes())
            self.consume(0, len(inp))

        ps = self.packet_size
        produced = 0
        max_output = (len(out) // ps) * ps

        if max_output < ps:
            return 0

        while produced + ps <= max_output:
            if len(self.buffer) < 2 * ps:
                break

            if not (self.buffer[0] == 0x47 and self.buffer[ps] == 0x47):
                sync_pos = self.find_sync_position()

                if sync_pos < 0:
                    keep = min(len(self.buffer), 2 * ps)
                    if len(self.buffer) > keep:
                        del self.buffer[:-keep]
                    break

                if sync_pos > 0:
                    del self.buffer[:sync_pos]

                if len(self.buffer) < 2 * ps:
                    break

            packet = bytes(self.buffer[:ps])
            out[produced:produced + ps] = np.frombuffer(packet, dtype=np.uint8)

            del self.buffer[:ps]
            produced += ps

        return produced