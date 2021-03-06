from __future__ import print_function

import argparse
import os
import pandas as pd

# sklearn.externals.joblib is deprecated in 0.21 and will be removed in 0.23. 
# from sklearn.externals import joblib
# Import joblib package directly
import joblib

## TODO: Import any additional libraries you need to define a model
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

# Provided model load function
def model_fn(model_dir):
    """Load model from the model_dir. This is the same model that is saved
    in the main if statement.
    """
    print("Loading model.")
    
    # load using joblib
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    print("Done loading model.")
    
    return model


## TODO: Complete the main code
if __name__ == '__main__':
    
    # All of the model parameters and training parameters are sent as arguments
    # when this script is executed, during a training job
    
    # Here we set up an argument parser to easily access the parameters
    parser = argparse.ArgumentParser()

    # SageMaker parameters, like the directories for training data and saving models; set automatically
    # Do not need to change
    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    
    ## TODO: Add any additional arguments that you will need to pass into your model
    
    # args holds all passed-in arguments
    args = parser.parse_args()

    # Read in csv training file
    training_dir = args.data_dir
    train_data = pd.read_csv(os.path.join(training_dir, "train.csv"), header=None, names=None)

    # Labels are in the first column
    #train_y = train_data.iloc[:,0]
    #train_x = train_data.iloc[:,1:]
    train_y = train_data.iloc[:,0].values.reshape(-1,1)
    train_x = train_data.iloc[:,1:].values
    
    ## --- Your code here --- ##
    classificator = SVC()
    param_grid = {'C': [1e3, 5e3, 1e4, 5e4], 'gamma': [0.0001, 0.005, 0.01, 0.1], }
    scoring = {'AUC': 'roc_auc', 'Accuracy': make_scorer(accuracy_score)}
    # Run the grid search
    grid_obj = GridSearchCV(classificator, param_grid, scoring=scoring, refit='AUC')
    grid_obj = grid_obj.fit(train_x, train_y)

    # Set the clf to the best combination of parameters
    model = grid_obj.best_estimator_

    # Fit the best algorithm to the data. 
    model.fit(train_x, train_y)
    
    


    ## TODO: Define a model 
    model = LinearSVC()
    
    
    ## TODO: Train the model
    model.fit(train_x, train_y)
    
    
    ## --- End of your code  --- ##
    

    # Save the trained model
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
