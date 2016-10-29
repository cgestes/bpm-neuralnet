#!/usr/bin/env python3
# coding: utf-8

# # Annotations for the Sirajology Python NN Example
#
# This code comes from a demo NN program from the YouTube video https://youtu.be/h3l4qz76JhQ. The program creates an neural network that simulates the exclusive OR function with two inputs and one output.
#
#

# In[1]:

import numpy as np  # Note: there is a typo on this line in the video

# The following is a function definition of the sigmoid function, which is the type of non-linearity chosen for this neural net. It is not the only type of non-linearity that can be chosen, but is has nice analytical features and is easy to teach with. In practice, large-scale deep learning systems use piecewise-linear functions because they are much less expensive to evaluate.
#
# The implementation of this function does double duty. If the deriv=True flag is passed in, the function instead calculates the derivative of the function, which is used in the error backpropogation step.

# In[2]:

def nonlin(x, deriv=False):  # Note: there is a typo on this line in the video
    if(deriv==True):
        return (x*(1-x))

    return 1/(1+np.exp(-x))  # Note: there is a typo on this line in the video


# The following code creates the input matrix. Although not mentioned in the video, the third column is for accommodating the bias term and is not part of the input.

# In[3]:

#input data
#1000 sample + 1 bias * 100 example

X = np.array([[0,0],  # Note: there is a typo on this line in the video
            [0,1],
            [1,0],
            [1,1]])


# The output of the exclusive OR function follows.

# In[4]:

#output data
#bpm of the track

y = np.array([[0],
             [1],
             [1],
             [0]])


print("ici")
import readdata
X, y = readdata.readData("who cares")
print("ici", X.shape, y.shape)


# The seed for the random generator is set so that it will return the same random numbers each time, which is sometimes useful for debugging.

# In[5]:

Number_Repete = 1
Number_Sample = len(X[1,:])
Number_Sample_Boucle = int(Number_Sample/Number_Repete)

Number_Exemple = len(y)

print("Nb sample", Number_Repete, Number_Sample, Number_Sample_Boucle)

# In[5]:

np.random.seed(1)


# Now we intialize the weights to random values. syn0 are the weights between the input layer and the hidden layer.  It is a 3x4 matrix because there are two input weights plus a bias term (=3) and four nodes in the hidden layer (=4). syn1 are the weights between the hidden layer and the output layer. It is a 4x1 matrix because there are 4 nodes in the hidden layer and one output. Note that there is no bias term feeding the output layer in this example. The weights are initially generated randomly because optimization tends not to work well when all the weights start at the same value. Note that neither of the neural networks shown in the video describe the example.

# In[6]:

#synapses
syn0 = 2*np.random.random((Number_Sample_Boucle+1,Number_Exemple)) - 1  # 21x100 matrix of weights ((20 inputs + 1 bias) x 100 nodes in the hidden layer)
syn1 = 2*np.random.random((Number_Exemple,1)) - 1  # 100x1 matrix of weights. (4 nodes x 1 output) - no bias term in the hidden layer.


# This is the main training loop. The output shows the evolution of the error between the model and desired. The error steadily decreases.

# In[7]:

#training step
for j in range(0,60000):
    for i in range(0,Number_Repete):
        # Calculate forward through the network.
        LO = np.ones([Number_Exemple,1]) #rajout du bias
        l0 = np.append(X[:,Number_Sample_Boucle*i:Number_Sample_Boucle*(i+1)],LO,axis=1)
        l1 = nonlin(np.dot(l0, syn0))
        l2 = nonlin(np.dot(l1, syn1))

        # Back propagation of errors using the chain rule.
        l2_error = y - l2
        #print ("Error: " + str(np.mean(np.abs(l2_error))))
        if (Number_Repete == 1):
            if ((j % 10000) == 0):   # Only print the error every 10000 steps, to save time and limit the amount of output.
                print ("Error: " + str(np.mean(np.abs(l2_error))))
        else:
            if ((j % 10000) == 0 and (i % Number_Repete-1) == 0):   # Only print the error every 10000 steps, to save time and limit the amount of output.
                print ("Error: " + str(np.mean(np.abs(l2_error))))

        l2_delta = l2_error*nonlin(l2, deriv=True)

        l1_error = l2_delta.dot(syn1.T)

        l1_delta = l1_error * nonlin(l1,deriv=True)

        #update weights (no learning rate term)
        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

print ("Output after training")
print (l2)




# See how the final output closely approximates the true output [0, 1, 1, 0]. If you increase the number of interations in the training loop (currently 60000), the final output will be even closer.


# In[ ]:
