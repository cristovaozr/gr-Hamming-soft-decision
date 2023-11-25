#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BER Data output to file
# Author: Cristóvão Rufino
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from custom_channel import custom_channel  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import ber_output_file_epy_block_0 as epy_block_0  # embedded python block
import ber_output_file_epy_block_1 as epy_block_1  # embedded python block



class ber_output_file(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "BER Data output to file", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("BER Data output to file")
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

        self.settings = Qt.QSettings("GNU Radio", "ber_output_file")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.noise_voltage = noise_voltage = 3

        ##################################################
        # Blocks
        ##################################################

        self.epy_block_1 = epy_block_1.blk()
        self.epy_block_0 = epy_block_0.blk()
        self.custom_channel_0 = custom_channel(
            noise_voltage=noise_voltage,
        )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '/home/cristovaozr/workspace/Doutorado/cce/gr-Hamming-soft-decision/ProjetoFinal/output-noisy-file.bin', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/cristovaozr/workspace/Doutorado/cce/gr-Hamming-soft-decision/ProjetoFinal/output-orig-file.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_random_uniform_source_x_0 = analog.random_uniform_source_b(0, 2, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.custom_channel_0, 1))
        self.connect((self.analog_random_uniform_source_x_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.analog_random_uniform_source_x_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.custom_channel_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_0, 0), (self.custom_channel_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_file_sink_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ber_output_file")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage
        self.custom_channel_0.set_noise_voltage(self.noise_voltage)




def main(top_block_cls=ber_output_file, options=None):

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
