#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: task6SdrRx
# Author: popo
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import sip



class task6SdrRx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "task6SdrRx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("task6SdrRx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "task6SdrRx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.sym_rate = sym_rate = 25000
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.alpha = alpha = 0.22
        self.tx_offset = tx_offset = 400000
        self.timing_loop_bw = timing_loop_bw = 0.03
        self.sdr_samp_rate = sdr_samp_rate = 2000000
        self.samp_rate_0 = samp_rate_0 = 32000
        self.rx_xlate = rx_xlate = 451000
        self.rx_gain = rx_gain = 0
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), alpha, 11*sps*nfilts)
        self.rrc_alpha = rrc_alpha = 0.35
        self.rf_freq = rf_freq = 915e6
        self.fine_rx = fine_rx = 0
        self.const = const = digital.constellation_16qam().base()
        self.const.set_npwr(1.0)
        self.bb_samp_rate = bb_samp_rate = sym_rate*sps
        self.M_qam = M_qam = 16

        ##################################################
        # Blocks
        ##################################################

        self._rx_gain_range = qtgui.Range(0, 10000, 1, 0, 200)
        self._rx_gain_win = qtgui.RangeWidget(self._rx_gain_range, self.set_rx_gain, "'rx_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_gain_win)
        self._fine_rx_range = qtgui.Range(-1000000, 1000000, 1, 0, 200)
        self._fine_rx_win = qtgui.RangeWidget(self._fine_rx_range, self.set_fine_rx, "'fine_rx'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fine_rx_win)
        self.soapy_rtlsdr_source_0 = None
        dev = 'driver=rtlsdr'
        stream_args = 'bufflen=16384'
        tune_args = ['']
        settings = ['']

        def _set_soapy_rtlsdr_source_0_gain_mode(channel, agc):
            self.soapy_rtlsdr_source_0.set_gain_mode(channel, agc)
            if not agc:
                  self.soapy_rtlsdr_source_0.set_gain(channel, self._soapy_rtlsdr_source_0_gain_value)
        self.set_soapy_rtlsdr_source_0_gain_mode = _set_soapy_rtlsdr_source_0_gain_mode

        def _set_soapy_rtlsdr_source_0_gain(channel, name, gain):
            self._soapy_rtlsdr_source_0_gain_value = gain
            if not self.soapy_rtlsdr_source_0.get_gain_mode(channel):
                self.soapy_rtlsdr_source_0.set_gain(channel, gain)
        self.set_soapy_rtlsdr_source_0_gain = _set_soapy_rtlsdr_source_0_gain

        def _set_soapy_rtlsdr_source_0_bias(bias):
            if 'biastee' in self._soapy_rtlsdr_source_0_setting_keys:
                self.soapy_rtlsdr_source_0.write_setting('biastee', bias)
        self.set_soapy_rtlsdr_source_0_bias = _set_soapy_rtlsdr_source_0_bias

        self.soapy_rtlsdr_source_0 = soapy.source(dev, "fc32", 1, '0',
                                  stream_args, tune_args, settings)

        self._soapy_rtlsdr_source_0_setting_keys = [a.key for a in self.soapy_rtlsdr_source_0.get_setting_info()]

        self.soapy_rtlsdr_source_0.set_sample_rate(0, sdr_samp_rate)
        self.soapy_rtlsdr_source_0.set_frequency(0, rf_freq)
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, 0)
        self.set_soapy_rtlsdr_source_0_bias(bool(False))
        self._soapy_rtlsdr_source_0_gain_value = 32
        self.set_soapy_rtlsdr_source_0_gain_mode(0, bool(False))
        self.set_soapy_rtlsdr_source_0_gain(0, 'TUNER', 32)
        self.qtgui_const_sink_x_0_1_0 = qtgui.const_sink_c(
            1024, #size
            "poly", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_1_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_1_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_1_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_1_0.enable_grid(False)
        self.qtgui_const_sink_x_0_1_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_1_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_1_0_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(20, firdes.low_pass(1.0, sdr_samp_rate, 40000, 1000), (-rx_xlate), sdr_samp_rate)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, timing_loop_bw, rrc_taps, nfilts, (nfilts/2), 1.5, 1)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((2*3.141592653589793*fine_rx/bb_samp_rate), False)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(rx_gain)
        # Create the options list
        self._M_qam_options = [8, 16, 32, 64, 128, 256]
        # Create the labels list
        self._M_qam_labels = ['8-QAM', '16-QAM', '32-QAM', '64-QAM', '128-QAM', '256-QAM']
        # Create the combo box
        self._M_qam_tool_bar = Qt.QToolBar(self)
        self._M_qam_tool_bar.addWidget(Qt.QLabel("Order M-QAM" + ": "))
        self._M_qam_combo_box = Qt.QComboBox()
        self._M_qam_tool_bar.addWidget(self._M_qam_combo_box)
        for _label in self._M_qam_labels: self._M_qam_combo_box.addItem(_label)
        self._M_qam_callback = lambda i: Qt.QMetaObject.invokeMethod(self._M_qam_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._M_qam_options.index(i)))
        self._M_qam_callback(self.M_qam)
        self._M_qam_combo_box.currentIndexChanged.connect(
            lambda i: self.set_M_qam(self._M_qam_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._M_qam_tool_bar)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_const_sink_x_0_1_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "task6SdrRx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sym_rate(self):
        return self.sym_rate

    def set_sym_rate(self, sym_rate):
        self.sym_rate = sym_rate
        self.set_bb_samp_rate(self.sym_rate*self.sps)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_bb_samp_rate(self.sym_rate*self.sps)
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.alpha, 11*self.sps*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.alpha, 11*self.sps*self.nfilts))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.alpha, 11*self.sps*self.nfilts))

    def get_tx_offset(self):
        return self.tx_offset

    def set_tx_offset(self, tx_offset):
        self.tx_offset = tx_offset

    def get_timing_loop_bw(self):
        return self.timing_loop_bw

    def set_timing_loop_bw(self, timing_loop_bw):
        self.timing_loop_bw = timing_loop_bw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.timing_loop_bw)

    def get_sdr_samp_rate(self):
        return self.sdr_samp_rate

    def set_sdr_samp_rate(self, sdr_samp_rate):
        self.sdr_samp_rate = sdr_samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1.0, self.sdr_samp_rate, 40000, 1000))
        self.soapy_rtlsdr_source_0.set_sample_rate(0, self.sdr_samp_rate)

    def get_samp_rate_0(self):
        return self.samp_rate_0

    def set_samp_rate_0(self, samp_rate_0):
        self.samp_rate_0 = samp_rate_0

    def get_rx_xlate(self):
        return self.rx_xlate

    def set_rx_xlate(self, rx_xlate):
        self.rx_xlate = rx_xlate
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((-self.rx_xlate))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.blocks_multiply_const_vxx_0.set_k(self.rx_gain)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)

    def get_rrc_alpha(self):
        return self.rrc_alpha

    def set_rrc_alpha(self, rrc_alpha):
        self.rrc_alpha = rrc_alpha

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq
        self.soapy_rtlsdr_source_0.set_frequency(0, self.rf_freq)

    def get_fine_rx(self):
        return self.fine_rx

    def set_fine_rx(self, fine_rx):
        self.fine_rx = fine_rx
        self.blocks_rotator_cc_0.set_phase_inc((2*3.141592653589793*self.fine_rx/self.bb_samp_rate))

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_bb_samp_rate(self):
        return self.bb_samp_rate

    def set_bb_samp_rate(self, bb_samp_rate):
        self.bb_samp_rate = bb_samp_rate
        self.blocks_rotator_cc_0.set_phase_inc((2*3.141592653589793*self.fine_rx/self.bb_samp_rate))

    def get_M_qam(self):
        return self.M_qam

    def set_M_qam(self, M_qam):
        self.M_qam = M_qam
        self._M_qam_callback(self.M_qam)




def main(top_block_cls=task6SdrRx, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
