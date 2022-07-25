import pandas as pd
import numpy as np
import scipy.stats as stats


def fratio_comparison(
    sc_exp_path,
    bulk_exp_path,
    output_path
    ):  
    
    """Compute ANOVA F and p value
    
    Keyword arguments:
    sc_exp_path -- path of single-cell expression matrix (tab-separated file)
    bulk_exp_path -- path of bulk expression matrix (tab-separated file)
    output_path -- path of output file containing F and p value (tab-separated file)
    """
    
    
    ## Import data
    
    # bulk expression matrix
    bulk = pd.read_table(
        bulk_exp_path, 
        index_col = 0
    )
    
    # single-cell expression matrix
    sc = pd.read_table(
        sc_exp_path, 
        index_col = 0
    )
    
    
    ## Data wrangling
    
    # remove genes with all 0s
    bulk_sub = bulk.loc[:, (bulk != 0).any(axis = 0)]
    sc_sub = sc.loc[:, (sc != 0).any(axis = 0)]
    
    # common genes between bulk and single cell
    common_genes = np.intersect1d(
        sc_sub.columns, 
        bulk.columns
    )
    
    # subset bulk and sc datasets by common genes
    bulk_common = bulk_sub.loc[:, common_genes]
    sc_common = sc_sub.loc[:, common_genes]
    
    
    ## F ratio computation
    
    # initialize empty dictionary
    fratio_d = {}
    
    for i in range(len(sc_common.columns)):
        
        # sc and bulk expression of gene i (pandas series)
        sc_gene = sc_common.iloc[:, i] 
        bulk_gene = bulk_common.iloc[:, i]
        
        # remove 0s from series in sc and bulk
        sc_gene_no_zero = sc_gene[sc_gene != 0]
        bulk_gene_no_zero = bulk_gene[bulk_gene != 0]
        
        # compute ANOVA F ratio and pvalue 
        fvalue, pvalue = stats.f_oneway(
            sc_gene_no_zero, 
            bulk_gene_no_zero
        )
        
        # add to dictionary
        fratio_d[sc_common.columns[i]] = fvalue, pvalue
        
    
    # make dataframe with ANOVA f ratio and pvalue 
    fratio_df = pd.DataFrame(
        fratio_d, 
        index = ['f_ratio', 'pvalue']).transpose()
    
    # and sort i by fratio value
    fratio_df_sort = fratio_df.sort_values(
        by = 'f_ratio',
        ascending = False)
    
    # save dataframe
    fratio_df_sort.to_csv(
        output_path, 
        sep = '\t', 
        index_label = 'genes'
    )