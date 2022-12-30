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
right_ans = x@w

# Read paramters in 'simconfig'
params = simulator.Parameterinput()

# SIM
HWsim = simulator.SystemSim(params)
output = HWsim.mvm(w,x)
assert (right_ans-output).sum() < 1, "not right"
HWsim.HWEvaluate()
HWsim.show()
