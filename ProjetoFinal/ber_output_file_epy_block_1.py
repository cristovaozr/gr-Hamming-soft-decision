"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='BPSK Demodulator',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.byte]
        )

    def work(self, input_items, output_items):
        for i, item in enumerate(input_items[0]):
            if item.real < 0:
                output_items[0][i] = 0
            else:
                output_items[0][i] = 1

        return len(output_items[0])
