import simulator
import numpy as np

'''

TODO Support CNN in the Hardware Evaluation 
'''

weights_dir = "./data/mnist-lenet.npz" 
# image_dir = "./data/dataset/mnist/test.npy"
batch_size = 10 # The number of input picture
weights = np.load(weights_dir, encoding="latin1")['arr_0'].item()
# data = np.load(image_dir, encoding="latin1")[:batch_size]
images = np.load("test_images_100.npy")
labels = np.load("test_labels_100.npy")

params = simulator.Parameterinput() # Read parameters in simconfig

# Define the neural network
net = [
    ['Conv2d',],
    ['Conv2d',],
    ['Linear',],
    ['Linear',],
    ['Linear',],
    ]

# SIM
HWsim = simulator.SystemSim(params) 
HWsim.apply(net, weights, images, labels) # Forward computing
HWsim.HWEvaluate()
HWsim.show() # Show the result in console
