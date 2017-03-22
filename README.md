# Eye-Movement-Classification
Detect neurologically atypical behavior from eye movements

MATLAB directory contains all the code for classlification of subjects into different categories 
  - contains code for feature generation
  - Recursive feature elimination
  - SVM

Python directory contains the code for Recurrent Neural Network for Attention Modeling. Contains code for following
  - creating a task object which handles reading/parsing/preprocessing data and starting the training procedure
  - creating a model object
  - creating an optimizer object for optimization (eg: sgd)
  - creating a Solver object which performs: training the model and sampling from the model
  - vars.py contains all the variables used for data input, training and everything required for the code to execute
    only change this file if don't want to look at the underlying code.
