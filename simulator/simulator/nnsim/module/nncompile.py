# nncompile.py

from __future__ import print_function, division
import numpy as np

class NNcompile(object):

    def __init__(self, params):
        super(NNcompile, self).__init__()

        self.params = params
        self.Gmax = params.Gmax
        self.Gmin = params.Gmin
        self.ReadVoltage = params.ReadVoltage
        self.numCol = params.numCol
        self.numRow = params.numRow
        self.WeightBits = params.WeightBits
        self.CellBits = params.CellBits
        self.IOBits = params.IOBits
        self.numCoreVMax = params.numCoreVMax
        self.numCoreHMax = params.numCoreHMax
        self.ReadPulseWidth = params.ReadPulseWidth
        self.numCellperWeight = params.numCellperWeight
        self.numLayerOutput = params.numLayerOutput
        if self.params.isPreciseNonnegative:
          self.RangeMax = 2 ** self.WeightBits - 1
          # [0, self.RangeMax]
        else:  
          self.RangeMax = 2 ** (self.WeightBits - 1) # The range of bitwise weight
          #is from -self.RangeMax to (self.RangeMax-1)
        self.Gstep = (self.Gmax-self.Gmin) / (2**self.CellBits - 1)
        

    def apply(self, Weight):
        """
        Map the weights to arrays.
        require args:
            Weight: The weights of a layer (float), include weight & bias
        """
        self.numLayerOutput = Weight.shape[1]# The number of outputs in the layer
        if self.params.isPreciseNonnegative:
          # 检查是否符合条件
          assert Weight.dtype == np.dtype('int64')
          assert Weight.min()>=0,"has negative value"
          assert Weight.max()<=self.RangeMax

        else: 
          WeightMax = max(Weight.max(), abs(Weight.min()))
          # Map to range (-self.RangeMax -- (self.RangeMax-1))
          Weight = np.round(Weight/WeightMax * self.RangeMax)
          Weight = np.where(Weight > (self.RangeMax-1), self.RangeMax-1, Weight)
          # Shift Weight to postive
          Weight += self.RangeMax
          Weight = np.abs(Weight)
        # When using more than 1 cell to represent weight, the weight should 
        # be spilt.
        if self.numCellperWeight > 1: # 成立, 为 2
            Weight = Weight.T # (1250,801)
            WeightSp = []
            Base = np.asarray([(2**self.CellBits)**x 
                for x in range(self.numCellperWeight-1, -1, -1)]) # [16,1]
            for i in range(Weight.shape[0]):
                for j in range(self.numCellperWeight):
                    SpiltTmp = Weight[i] // Base[j]
                    Weight[i] = Weight[i] % Base[j]
                    WeightSp.append(SpiltTmp)
            WeightSp = np.asarray(WeightSp)
            Weight = WeightSp.T
        # Compile the weights to arrays
        numCoreV = int(np.ceil(Weight.shape[0]/self.numRow)) # 4
        if self.params.isPreciseNonnegative:
          numCoreH = int(np.ceil(Weight.shape[1]/self.numCol))
          numOutput = numCoreH * self.numCol
        else:
          numCoreH = int(np.ceil(Weight.shape[1]/(self.numCol-self.numCellperWeight))) # 10
          numOutput = numCoreH * (self.numCol-self.numCellperWeight)
        CoresInfo = (numCoreV, numCoreH)
        numInput = numCoreV * self.numRow
        WeightMap = np.concatenate(
                (np.zeros((numInput-Weight.shape[0], Weight.shape[1])), Weight),
                axis=0)
        WeightMap = np.concatenate(
                (WeightMap, np.zeros((numInput, (numOutput - Weight.shape[1])))),
                axis=1) # prefill the array blanks
        WeightVsp = np.vsplit(WeightMap, numCoreV)
        for i in range(numCoreV):
            WeightHsp = np.hsplit(WeightVsp[i], numCoreH)
            if not self.params.isPreciseNonnegative:
              for j in range(numCoreH):
                  WeightHsp[j] = np.concatenate(
                          (WeightHsp[j],
                              2**(self.CellBits-1) * np.ones((self.numRow, 1)),
                              np.zeros((self.numRow, self.numCellperWeight-1))
                              ),
                          axis=1)
            WeightVsp[i] = WeightHsp
        Weight = WeightVsp

        # Map to conductance
        
        for i in range(numCoreV):
            for j in range(numCoreH):
                Weight[i][j] = self.Gmin + self.Gstep*Weight[i][j]
                # Weight2 = Weight[i][j]

                # RRAM model: add write and read noise
                if not self.params.isPreciseNonnegative:
                    coeff = [ -6.0e-4, 6.2e-2, 7.2e-1]
                    WeightSD = coeff[0]*(Weight[i][j]*1e6)*(Weight[i][j]*1e6) +\
                            coeff[1]*(Weight[i][j]*1e6) + coeff[2]
                    WeightSD = WeightSD * 1e-6
    #                print(np.random.randn(self.numRow,self.numCol)*WeightSD)
                    Weight[i][j] = np.random.randn(self.numRow,
                            self.numCol)*WeightSD + Weight[i][j]

        return Weight, CoresInfo

