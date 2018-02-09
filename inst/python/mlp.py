#  Neural network classification with n fold cross validation
#===============================================================
# INPUT:
# 1) location of files: libsvm file + indexes file (rowId, index)
# 2) 
#
# OUTPUT:
# it returns a file with indexes merged with prediction for test index  
#================================================================
import numpy as np
#from collections import OrderedDict
import os
import sys
import timeit
import math
from sklearn.neural_network import MLPClassifier
from scipy.sparse import coo_matrix,csr_matrix,vstack,hstack
#from sklearn.feature_selection import SelectFromModel
from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
from sklearn.externals import joblib

#================================================================
print "Training Neural Network model " 

y = population[:,1]
X = plpData[population[:,0],:]
trainInds =population[:,population.shape[1]-1] >0

print "Dataset has %s rows and %s columns" %(X.shape[0], X.shape[1])
print "population loaded- %s rows and %s columns" %(np.shape(population)[0], np.shape(population)[1])
###########################################################################

if train:
  pred_size = int(np.sum(population[:,population.shape[1]-1] > 0))
  print "Calculating prediction for train set of size %s" %(pred_size)
  test_pred = np.zeros(pred_size)# zeros length sum(population[:,population.size[1]] ==i)
  for i in range(1, int(np.max(population[:,population.shape[1]-1])+1), 1):
    testInd =population[population[:,population.shape[1]-1] > 0,population.shape[1]-1] ==i
    trainInd = (population[population[:,population.shape[1]-1] > 0,population.shape[1]-1] !=i)
    train_x = X[trainInds,:][trainInd,:]
    train_y = y[trainInds][trainInd]
  
    test_x = X[trainInds,:][testInd,:]	
    print "Fold %s split %s in train set and %s in test set" %(i, train_x.shape[0], test_x.shape[0])
    print "Train set contains %s outcomes " %(np.sum(train_y))

    # train on fold
    print "Training fold %s" %(i)
    start_time = timeit.default_timer()	
    mlp = MLPClassifier(activation='logistic', alpha=alpha, learning_rate='adaptive', hidden_layer_sizes=(size, 2), random_state=seed)
    mlp = mlp.fit(train_x, train_y)
    end_time = timeit.default_timer()
    print "Training fold took: %.2f s" %(end_time-start_time)
    print "Calculating predictions on left out fold set..."
    ind = (population[:,population.shape[1]-1] > 0)
    ind = population[ind,population.shape[1]-1]==i
    test_pred[ind] = mlp.predict_proba(test_x)[:,1]
    print "Prediction complete: %s rows " %(np.shape(test_pred[ind])[0])
    print "Mean: %s prediction value" %(np.mean(test_pred[ind]))
   
  # merge pred with indexes[testInd,:]
  test_pred.shape = (population[population[:,population.shape[1]-1] > 0,:].shape[0], 1)
  prediction = np.append(population[population[:,population.shape[1]-1] > 0,:],test_pred, axis=1)


# train final:
else:
  print "Training final neural network model on all train data..."
  print "X- %s rows and Y %s length" %(X[trainInds,:].shape[0], y[trainInds].shape[0])

  start_time = timeit.default_timer()	
  mlp = MLPClassifier(activation='logistic', alpha=alpha,learning_rate='adaptive', hidden_layer_sizes=(size, 2), random_state=seed, tol=0.0000001)
  mlp = mlp.fit(X[trainInds,:], y[trainInds])
  end_time = timeit.default_timer()
  print "Training final took: %.2f s" %(end_time-start_time)
	
  # save the model:
  if not os.path.exists(modelOutput):
      os.makedirs(modelOutput)
  print "Model saved to: %s" %(modelOutput)	
  joblib.dump(mlp, os.path.join(modelOutput,'model.pkl'))
