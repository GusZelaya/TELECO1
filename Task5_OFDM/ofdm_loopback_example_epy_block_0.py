import pmt
import numpy as np
from gnuradio import gr

class blk(gr.basic_block):
    """
    Divide cualquier PDU entrante en PDUs MPEG-TS de 188 bytes.
    Entrada: mensajes PDU desde Socket PDU.
    Salida: mensajes PDU de exactamente 188 bytes.
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name="pdu_ts_splitter_188",
            in_sig=[],
            out_sig=[]
        )

        self.packet_size = 188
        self.buffer = bytearray()

        self.message_port_register_in(pmt.intern("pdus"))
        self.message_port_register_out(pmt.intern("pdus"))
        self.set_msg_handler(pmt.intern("pdus"), self.handle_pdu)

    def handle_pdu(self, msg):
        if not pmt.is_pair(msg):
            return

        meta = pmt.car(msg)
        vec = pmt.cdr(msg)

        if not pmt.is_u8vector(vec):
            return

        data = bytes(pmt.u8vector_elements(vec))
        self.buffer.extend(data)

        ps = self.packet_size

        while len(self.buffer) >= ps:
            # Buscar sincronismo MPEG-TS 0x47.
            if self.buffer[0] != 0x47:
                sync_pos = self.buffer.find(0x47)

                if sync_pos < 0:
                    # No hay sincronismo; conservar pocos bytes por seguridad.
                    self.buffer = self.buffer[-ps:]
                    return

                del self.buffer[:sync_pos]

                if len(self.buffer) < ps:
                    return

            packet = bytes(self.buffer[:ps])
            del self.buffer[:ps]

            out_vec = pmt.init_u8vector(ps, list(packet))
            out_msg = pmt.cons(meta, out_vec)

            self.message_port_pub(pmt.intern("pdus"), out_msg)