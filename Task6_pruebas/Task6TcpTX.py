#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: popo
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
import Task6TcpTX_epy_block_0 as epy_block_0  # embedded python block
import sip



class Task6TcpTX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "Task6TcpTX")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.variable_0_0 = variable_0_0 = 0
        self.samp_rate_0 = samp_rate_0 = 32000
        self.samp_rate = samp_rate = 32000
        self.noise_amp = noise_amp = 0.0
        self.byte_rate = byte_rate = 20000
        self.M_qam = M_qam = 16

        ##################################################
        # Blocks
        ##################################################

        self._noise_amp_range = qtgui.Range(0.0, 0.5, 0.01, 0.0, 200)
        self._noise_amp_win = qtgui.RangeWidget(self._noise_amp_range, self.set_noise_amp, "Amplitud AWGN", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_amp_win)
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
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


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
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_gr_complex, 1, '127.0.0.1', 6000,1)
        self.epy_block_0 = epy_block_0.blk(M_qam=M_qam)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, byte_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * byte_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(noise_amp)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/popo/Escritorio/Task6_pruebas/task6_imagen_prueba.png', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.network_tcp_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_throttle2_0, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_const_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Task6TcpTX")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_0_0(self):
        return self.variable_0_0

    def set_variable_0_0(self, variable_0_0):
        self.variable_0_0 = variable_0_0

    def get_samp_rate_0(self):
        return self.samp_rate_0

    def set_samp_rate_0(self, samp_rate_0):
        self.samp_rate_0 = samp_rate_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp
        self.blocks_multiply_const_vxx_0.set_k(self.noise_amp)

    def get_byte_rate(self):
        return self.byte_rate

    def set_byte_rate(self, byte_rate):
        self.byte_rate = byte_rate
        self.blocks_throttle2_0.set_sample_rate(self.byte_rate)

    def get_M_qam(self):
        return self.M_qam

    def set_M_qam(self, M_qam):
        self.M_qam = M_qam
        self._M_qam_callback(self.M_qam)
        self.epy_block_0.M_qam = self.M_qam




def main(top_block_cls=Task6TcpTX, options=None):

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
