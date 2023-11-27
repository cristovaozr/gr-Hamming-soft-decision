#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: cristovaozr
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



class ber_bpsk_externo(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "ber_bpsk_externo")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10000000

        ##################################################
        # Blocks
        ##################################################

        self.bpsk_ber_generator_0 = bpsk_ber_generator()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_vector_0_6 = blocks.stream_to_vector(gr.sizeof_char*1, 8)
        self.blocks_stream_to_vector_0_5 = blocks.stream_to_vector(gr.sizeof_char*1, 8)
        self.blocks_stream_to_vector_0_4 = blocks.stream_to_vector(gr.sizeof_char*1, 8)
        self.blocks_stream_to_vector_0_3 = blocks.stream_to_vector(gr.sizeof_char*1, 8)
        self.blocks_stream_to_vector_0_2 = blocks.stream_to_vector(gr.sizeof_char*1, 8)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_char*1, 8)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_char*1, 8)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_char*1, 8)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, 8)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_char*1)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_2 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_file_sink_0_0_3 = blocks.file_sink(gr.sizeof_char*8, '/tmp/snr6db.bin', False)
        self.blocks_file_sink_0_0_3.set_unbuffered(False)
        self.blocks_file_sink_0_0_2 = blocks.file_sink(gr.sizeof_char*8, '/tmp/snr4db.bin', False)
        self.blocks_file_sink_0_0_2.set_unbuffered(False)
        self.blocks_file_sink_0_0_1 = blocks.file_sink(gr.sizeof_char*8, '/tmp/snr2db.bin', False)
        self.blocks_file_sink_0_0_1.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_2 = blocks.file_sink(gr.sizeof_char*8, '/tmp/snr7db.bin', False)
        self.blocks_file_sink_0_0_0_2.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_1 = blocks.file_sink(gr.sizeof_char*8, '/tmp/snr5db.bin', False)
        self.blocks_file_sink_0_0_0_1.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_0 = blocks.file_sink(gr.sizeof_char*8, '/tmp/snr3db.bin', False)
        self.blocks_file_sink_0_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_char*8, '/tmp/snr1db.bin', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*8, '/tmp/snr0db.bin', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*8, '/tmp/bytes_originais.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_null_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.blocks_file_sink_0_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_2, 0), (self.blocks_file_sink_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_3, 0), (self.blocks_file_sink_0_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0_4, 0), (self.blocks_file_sink_0_0_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_5, 0), (self.blocks_file_sink_0_0_3, 0))
        self.connect((self.blocks_stream_to_vector_0_6, 0), (self.blocks_file_sink_0_0_0_2, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.bpsk_ber_generator_0, 2), (self.blocks_null_sink_0, 0))
        self.connect((self.bpsk_ber_generator_0, 4), (self.blocks_null_sink_0_0, 0))
        self.connect((self.bpsk_ber_generator_0, 10), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.bpsk_ber_generator_0, 6), (self.blocks_null_sink_0_1, 0))
        self.connect((self.bpsk_ber_generator_0, 12), (self.blocks_null_sink_0_1_0, 0))
        self.connect((self.bpsk_ber_generator_0, 14), (self.blocks_null_sink_0_1_0_0, 0))
        self.connect((self.bpsk_ber_generator_0, 8), (self.blocks_null_sink_0_2, 0))
        self.connect((self.bpsk_ber_generator_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.bpsk_ber_generator_0, 1), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.bpsk_ber_generator_0, 3), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.bpsk_ber_generator_0, 5), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.bpsk_ber_generator_0, 7), (self.blocks_stream_to_vector_0_2, 0))
        self.connect((self.bpsk_ber_generator_0, 9), (self.blocks_stream_to_vector_0_3, 0))
        self.connect((self.bpsk_ber_generator_0, 11), (self.blocks_stream_to_vector_0_4, 0))
        self.connect((self.bpsk_ber_generator_0, 13), (self.blocks_stream_to_vector_0_5, 0))
        self.connect((self.bpsk_ber_generator_0, 15), (self.blocks_stream_to_vector_0_6, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ber_bpsk_externo")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)




def main(top_block_cls=ber_bpsk_externo, options=None):

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
