I started out by basing the network on the handwriting example as it was a functional image classification neural network. I expected it to work similarly.

However, it was not training at all, so I had to tune the numbers.

The first thing I tried was making the convolutional layers and hidden layers larger and larger. This did increase accuracy, but made the training unreasonably slow.

I then changed my approach by adding extra convolutional and pooling layers instead of just making them larger. This improved accuracy with far less cost in training time. I then made the hidden layer a litter larger and got to the final model.