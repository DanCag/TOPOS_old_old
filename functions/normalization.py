## Import packages ##

import pandas as pd
import numpy as np
from sklearn.preprocessing import scale


# normalize testing dataset
def normalize(
    training_exp,
    testing_exp_path,
    gene_list_path = ''):
    
    """Normalize testing dataset
    
    Keyword arguments
    training_exp_path -- training expression matrix
    testing_exp_path -- path of testing expression matrix samples x entrez gene id (tab-separated file)
    gene_list_path -- path of gene list file (tab-separated file)
    """
    
    
    ## Import data
        
    # testing #
    
    # testing matrix
    testing = pd.read_table(
        testing_exp_path,
        index_col = 0)
    
    
    ## Data wrangling
    
    # if path is not empty
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
            testing.columns.to_numpy() # numpy array of genes in testing matrix
        )

        # intersection of genes in list and training and testing matrixes
        common_genes = np.intersect1d(
            gene_list['gene'].to_numpy(),# numpy array of genes in gene list
            training_testing_genes
        )
        
        # subset training
        training_common = training_exp.loc[:, common_genes]
        
        # subset testing
        testing_common = testing.loc[:, common_genes]
    
    else:
        
        # intersection of genes in list, training and testing matrixes
        common_genes = np.intersect1d(
            training_exp.columns.to_numpy(), # numpy array of genes in training matrix
            testing.columns.to_numpy() # numpy array of genes in testing matrix
        )

        # subset training
        training_common = training_exp.loc[:, common_genes]
        
        # subset testing
        testing_common = testing.loc[:, common_genes]
        
        
    ## Normalization
    
    # Scale datasets sample-wise
    
    # training
    x_train_sw = pd.DataFrame(
        scale(
            X = training_common, 
            axis = 1), 
        index = training_common.index, 
        columns = training_common.columns)
    
    # testing
    x_test_sw = pd.DataFrame(
        scale(
            X = testing_common, 
            axis = 1), 
        index = testing_common.index, 
        columns = testing_common.columns)
    
    # Mean - stardard deviation table of training matrix
    
    # mean - sd table
    mean_sd = pd.concat(
        [x_train_sw.mean(), 
         x_train_sw.std()], 
        axis = 1)
    
    # table columns names
    mean_sd.columns = ['mean', 'sd']
    
    
    # Scale testing dataset feature wise
    x_test_sw_fw = pd.DataFrame(
        (x_test_sw - mean_sd.loc[x_test_sw.columns,'mean'])/(mean_sd.loc[x_test_sw.columns,'sd']),
        index = testing_common.index, 
        columns = testing_common.columns)
    
    return x_test_sw_fw