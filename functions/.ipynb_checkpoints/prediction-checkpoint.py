import pandas as pd
import numpy as np


# tumor detector predictions
def predict( 
    testing_nrmlz,
    clf,
    encdr,
    prediction_file):
    
    """Predict either tumor vs non-tumor or TOO
    
    Keyword arguments
    testing_nrmlz -- sample-wise + feature-wise normalized testing matrix
    clf -- trained classifier object
    encdr -- encoder object
    prediction_file -- path of prediction file (tab-separated file)
    """
    
    
    ## Import data
    
        
    ## Predict
    
    # predictions dataframe
    preds = pd.Series(
        encdr.inverse_transform(
            clf.predict(testing_nrmlz)), 
        index = testing_nrmlz.index, 
        name = "best_prediction")
    
    # write prediction to tsv file
    preds.to_csv(
        prediction_file,
        sep = '\t')