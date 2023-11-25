#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Deep Space Modulation Simulator
# Author: Cristóvão, José Ribamar e Robson
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from bpsk_ber_generator import bpsk_ber_generator  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from rs_ber_generator2 import rs_ber_generator2  # grc-generated hier_block
import sip
import numpy



class projeto_final(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Deep Space Modulation Simulator", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Deep Space Modulation Simulator")
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

        self.settings = Qt.QSettings("GNU Radio", "projeto_final")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 3200000
        self.num_curves = num_curves = 2
        self.esno = esno = numpy.arange(0, 8, 1)

        ##################################################
        # Blocks
        ##################################################

        self.rs_ber_generator2_0 = rs_ber_generator2()
        self.qtgui_bercurve_sink_0 = qtgui.ber_sink_b(
            esno, #range of esnos
            num_curves, #number of curves
            25, #ensure at least
            (-7.0), #cutoff
            ['RS(255,223)', 'BPSK AWGN'], #indiv. curve names
            None # parent
        )
        self.qtgui_bercurve_sink_0.set_update_time(0.10)
        self.qtgui_bercurve_sink_0.set_y_axis((-10), 0)
        self.qtgui_bercurve_sink_0.set_x_axis(esno[0], esno[-1])

        labels = ['RS(255,223)', 'BPSK AWGN', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]

        for i in range(num_curves):
            if len(labels[i]) == 0:
                self.qtgui_bercurve_sink_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_bercurve_sink_0.set_line_label(i, labels[i])
            self.qtgui_bercurve_sink_0.set_line_width(i, widths[i])
            self.qtgui_bercurve_sink_0.set_line_color(i, colors[i])
            self.qtgui_bercurve_sink_0.set_line_style(i, styles[i])
            self.qtgui_bercurve_sink_0.set_line_marker(i, markers[i])
            self.qtgui_bercurve_sink_0.set_line_alpha(i, alphas[i])

        self._qtgui_bercurve_sink_0_win = sip.wrapinstance(self.qtgui_bercurve_sink_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_bercurve_sink_0_win)
        self.bpsk_ber_generator_0 = bpsk_ber_generator()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_char*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_null_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.bpsk_ber_generator_0, 5), (self.qtgui_bercurve_sink_0, 21))
        self.connect((self.bpsk_ber_generator_0, 13), (self.qtgui_bercurve_sink_0, 29))
        self.connect((self.bpsk_ber_generator_0, 4), (self.qtgui_bercurve_sink_0, 20))
        self.connect((self.bpsk_ber_generator_0, 2), (self.qtgui_bercurve_sink_0, 18))
        self.connect((self.bpsk_ber_generator_0, 14), (self.qtgui_bercurve_sink_0, 30))
        self.connect((self.bpsk_ber_generator_0, 12), (self.qtgui_bercurve_sink_0, 28))
        self.connect((self.bpsk_ber_generator_0, 11), (self.qtgui_bercurve_sink_0, 27))
        self.connect((self.bpsk_ber_generator_0, 10), (self.qtgui_bercurve_sink_0, 26))
        self.connect((self.bpsk_ber_generator_0, 6), (self.qtgui_bercurve_sink_0, 22))
        self.connect((self.bpsk_ber_generator_0, 9), (self.qtgui_bercurve_sink_0, 25))
        self.connect((self.bpsk_ber_generator_0, 0), (self.qtgui_bercurve_sink_0, 16))
        self.connect((self.bpsk_ber_generator_0, 8), (self.qtgui_bercurve_sink_0, 24))
        self.connect((self.bpsk_ber_generator_0, 15), (self.qtgui_bercurve_sink_0, 31))
        self.connect((self.bpsk_ber_generator_0, 3), (self.qtgui_bercurve_sink_0, 19))
        self.connect((self.bpsk_ber_generator_0, 1), (self.qtgui_bercurve_sink_0, 17))
        self.connect((self.bpsk_ber_generator_0, 7), (self.qtgui_bercurve_sink_0, 23))
        self.connect((self.rs_ber_generator2_0, 12), (self.qtgui_bercurve_sink_0, 12))
        self.connect((self.rs_ber_generator2_0, 5), (self.qtgui_bercurve_sink_0, 5))
        self.connect((self.rs_ber_generator2_0, 3), (self.qtgui_bercurve_sink_0, 3))
        self.connect((self.rs_ber_generator2_0, 13), (self.qtgui_bercurve_sink_0, 13))
        self.connect((self.rs_ber_generator2_0, 7), (self.qtgui_bercurve_sink_0, 7))
        self.connect((self.rs_ber_generator2_0, 2), (self.qtgui_bercurve_sink_0, 2))
        self.connect((self.rs_ber_generator2_0, 4), (self.qtgui_bercurve_sink_0, 4))
        self.connect((self.rs_ber_generator2_0, 15), (self.qtgui_bercurve_sink_0, 15))
        self.connect((self.rs_ber_generator2_0, 9), (self.qtgui_bercurve_sink_0, 9))
        self.connect((self.rs_ber_generator2_0, 6), (self.qtgui_bercurve_sink_0, 6))
        self.connect((self.rs_ber_generator2_0, 8), (self.qtgui_bercurve_sink_0, 8))
        self.connect((self.rs_ber_generator2_0, 10), (self.qtgui_bercurve_sink_0, 10))
        self.connect((self.rs_ber_generator2_0, 11), (self.qtgui_bercurve_sink_0, 11))
        self.connect((self.rs_ber_generator2_0, 1), (self.qtgui_bercurve_sink_0, 1))
        self.connect((self.rs_ber_generator2_0, 0), (self.qtgui_bercurve_sink_0, 0))
        self.connect((self.rs_ber_generator2_0, 14), (self.qtgui_bercurve_sink_0, 14))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "projeto_final")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_num_curves(self):
        return self.num_curves

    def set_num_curves(self, num_curves):
        self.num_curves = num_curves

    def get_esno(self):
        return self.esno

    def set_esno(self, esno):
        self.esno = esno




def main(top_block_cls=projeto_final, options=None):

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
