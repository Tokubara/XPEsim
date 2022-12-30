# -*- coding: utf-8 -*-
#inputcompile.py

from __future__ import print_function, division
import numpy as np

class Inputcompile(object):
    def __init__(self, params):
        super(Inputcompile, self).__init__()
        
        self.params = params
        self.numRow = params.numRow
        self.IOBits = params.IOBits

    def apply(self, Input): 
        """
        Transport the input value to pulses, the input should be less than 2**IOBits.
        The output will be splited to different cores in the next layer
        require args:
            Input: The Inputs of a layer(BatchSize*H*W)
        """
        InputPulse = []
        if self.params.isPreciseNonnegative:
          numCoreNext = int(np.ceil( (Input[0].shape[0]) / self.numRow))
        else:
          numCoreNext = int(np.ceil( (Input[0].shape[0] + 1) / self.numRow))
        for sample in Input: # 784
            if self.params.isPreciseNonnegative:
              sample = np.concatenate( (np.zeros( int(self.numRow * numCoreNext) - 
                  sample.shape[0]), sample), axis=0) # 1023
            else:
              sample = np.concatenate( (np.zeros( int(self.numRow * numCoreNext - 1) - 
                  sample.shape[0]), sample), axis=0) # 1023
              # Add bias input(1)
              sample = np.concatenate( (sample, np.ones(1)), axis=0 ) # 1024
            sample = sample.reshape(-1, 1) # (1024,1)
            sampleVsp = np.vsplit(sample, numCoreNext) # list, 每一个元素是 (256,1)
            OutputVsp = []
            for i in range(numCoreNext):
                samplePerCore = []
                # Pulse[MSB : LSB]
                for j in range(self.IOBits-1, -1, -1):
                    samplePerBit = np.floor(sampleVsp[i]//(2**j))
                    samplePerCore.append(samplePerBit)
                    sampleVsp[i] = sampleVsp[i] % (2**j)
                OutputVsp.append(samplePerCore)
            InputPulse.append(OutputVsp)
        return InputPulse # 100, 4, 8, (256,1)

if __name__ == "__main__":
    pass

