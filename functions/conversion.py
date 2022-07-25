import pandas as pd

def conversion(
    testing_exp_path, 
    converted_exp_path):
    
    """Convert RPKM/FPKM into TPM
    
    Keyword arguments
    
    testing_exp_path -- path of testing expression matrix samples x entrez gene id (tab-separated file)
    converted_exp_path -- path of converted expression matrix (tab-separated file)
    """
    
    
    ## Import data
    
    # rpkm or fpkm dataset
    fpkm = pd.read_table(
        testing_exp_path, 
        index_col = 0
    )
    
    
    ## Conversion
    # rpkm/fpkm to tpm
    tpm = fpkm.apply(lambda x : (x/sum(x))*10**6, axis = 1)
    
    # save tpm converted testing dataset
    tpm.to_csv(
        converted_exp_path, 
        sep = '\t', 
        index_label = 'sample'
    )