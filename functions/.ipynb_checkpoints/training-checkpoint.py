## Import packages ##

import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import scale, LabelEncoder


# train tumor dector model
def train(
    training_exp,
    training_labels,
    testing_features, 
    gene_list_path = ''):
    
    """Train either tumor or TOO model
    
    Keyword arguments:
    training_exp -- training expression matrix
    training_labels -- training labels
    gene_list_path -- path of gene list file (tab-separated file)
    """
    
    
    ## Data wrangling
    
    # if gen list path is not empty
    if gene_list_path:
        
        # import gene list
        gene_list = pd.read_table(
            gene_list_path, 
            header = None, 
            names = ['gene'], 
            dtype = 'str')
        
        # intersection of genes in training and testing matrixes
        training_testing_genes = np.intersect1d(
            training_exp.columns.to_numpy(), # numpy array of genes in training matrix
            testing_features # numpy array of genes in testing matrix
        )

        # intersection of genes in list and training and testing matrixes
        common_genes = np.intersect1d(
            gene_list['gene'].to_numpy(),# numpy array of genes in gene list
            training_testing_genes
        )
        
        # subset training
        training_common = training_exp.loc[:, common_genes]
    
    else:
        
        # intersection of genes in list, training and testing matrixes
        common_genes = np.intersect1d(
            training_exp.columns.to_numpy(), # numpy array of genes in training matrix
            testing_features # numpy array of genes in testing matrix
        )

        # subset training
        training_common = training_exp.loc[:, common_genes]
       
        
    ## Normalization
    
    # Scale datasets sample-wise
    
    # training
    x_train_sw = pd.DataFrame(
        scale(
            X = training_common, 
            axis = 1), 
        index = training_common.index, 
        columns = training_common.columns)
    
    # Mean - stardard deviation table of training matrix
    
    # mean - sd table
    mean_sd = pd.concat(
        [x_train_sw.mean(), 
         x_train_sw.std()], 
        axis = 1)
    
    # table columns names
    mean_sd.columns = ['mean', 'sd']
    
    
    # Scale datasets feature wise
    x_train_sw_fw = pd.DataFrame(
        (x_train_sw - mean_sd.loc[x_train_sw.columns,'mean'])/(mean_sd.loc[x_train_sw.columns,'sd']),
        index = training_common.index,
        columns = training_common.columns)

    
    ## Build encoder
    encoder = LabelEncoder().fit(training_labels)

    # transform labels
    y_train = encoder.transform(training_labels)
    
    
    ## Train the model
    
    # train classifier
    clf = SVC(kernel = 'linear').fit(x_train_sw_fw, y_train)
    
    return encoder, clf
