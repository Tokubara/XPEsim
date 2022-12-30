import simulator
import numpy as np

'''
This example show the algorithm evaluation 
and hardware evaluation for MLP
'''

# Data pretreatment
# 先 256. 256
n = 256
w=np.random.randint(0, 255, (n,n))
x=np.random.randint(0, 10, (1,n))

# Read paramters in 'simconfig'
params = simulator.Parameterinput()

# SIM
HWsim = simulator.SystemSim(params)
HWsim.mvm(w,x)
HWsim.HWEvaluate()
HWsim.show()
