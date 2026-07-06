#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Task6SdrTx
# Author: popo
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
import numpy
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



class Task6SdrTx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Task6SdrTx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Task6SdrTx")
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

        self.settings = Qt.QSettings("GNU Radio", "Task6SdrTx")

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
        self.tx_offset = tx_offset = 400000
        self.sdr_samp_rate = sdr_samp_rate = 2000000
        self.samp_rate = samp_rate = 32000
        self.rx_xlate = rx_xlate = 413000
        self.rrc_alpha = rrc_alpha = 0.35
        self.rf_freq = rf_freq = 915e6
        self.const = const = digital.constellation_16qam().base()
        self.const.set_npwr(1.0)
        self.bb_samp_rate = bb_samp_rate = sym_rate*sps
        self.alpha = alpha = 0.22
        self.M_qam = M_qam = 16

        ##################################################
        # Blocks
        ##################################################

        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, '0',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, sdr_samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, rf_freq)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', 0)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(30, 0.0), 47.0))
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=20,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            sdr_samp_rate, #bw
            "me quiero morir", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-120), 0)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_0_1 = qtgui.const_sink_c(
            1024, #size
            "contelation modulator", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1.set_update_time(0.10)
        self.qtgui_const_sink_x_0_1.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_1.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_1.enable_autoscale(False)
        self.qtgui_const_sink_x_0_1.enable_grid(False)
        self.qtgui_const_sink_x_0_1.enable_axis_labels(True)


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
                self.qtgui_const_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_1_win = sip.wrapinstance(self.qtgui_const_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_1_win)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            1024, #size
            "hackrf", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis((-0.15), 0.15)
        self.qtgui_const_sink_x_0_0.set_x_axis((-0.15), 0.15)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


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
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_0_win)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=const,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=alpha,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((2*3.141592653589793*400000/2000000), False)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(0.15)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 100000))), True)
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
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.soapy_hackrf_sink_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.qtgui_const_sink_x_0_1, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_rotator_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Task6SdrTx")
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

    def get_tx_offset(self):
        return self.tx_offset

    def set_tx_offset(self, tx_offset):
        self.tx_offset = tx_offset

    def get_sdr_samp_rate(self):
        return self.sdr_samp_rate

    def set_sdr_samp_rate(self, sdr_samp_rate):
        self.sdr_samp_rate = sdr_samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.sdr_samp_rate)
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.sdr_samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rx_xlate(self):
        return self.rx_xlate

    def set_rx_xlate(self, rx_xlate):
        self.rx_xlate = rx_xlate

    def get_rrc_alpha(self):
        return self.rrc_alpha

    def set_rrc_alpha(self, rrc_alpha):
        self.rrc_alpha = rrc_alpha

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq
        self.soapy_hackrf_sink_0.set_frequency(0, self.rf_freq)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_bb_samp_rate(self):
        return self.bb_samp_rate

    def set_bb_samp_rate(self, bb_samp_rate):
        self.bb_samp_rate = bb_samp_rate

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_M_qam(self):
        return self.M_qam

    def set_M_qam(self, M_qam):
        self.M_qam = M_qam
        self._M_qam_callback(self.M_qam)




def main(top_block_cls=Task6SdrTx, options=None):

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
