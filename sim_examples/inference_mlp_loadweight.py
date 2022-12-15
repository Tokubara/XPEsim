import simulator
import numpy as np

'''
This example show the algorithm evaluation 
and hardware evaluation for MLP
'''

# Data pretreatment

weights_dir = "./data/mnist-lenet.npz" 
# image_dir = "./data/dataset/mnist/test.npy"
batch_size = 10 # The number of input picture
weights = np.load(weights_dir, encoding="latin1")['arr_0'].item()
# data = np.load(image_dir, encoding="latin1")[:batch_size]
images = np.load("test_images_100.npy")
labels = np.load("test_labels_100.npy")

# Read paramters in 'simconfig'
params = simulator.Parameterinput()

# Define the neural network
net = [
    ['Linear'],
    ['Linear'],
    ['Linear']
]

# SIM
HWsim = simulator.SystemSim(params)
HWsim.apply(net, weights, images, labels) 
HWsim.HWEvaluate()
HWsim.show()
