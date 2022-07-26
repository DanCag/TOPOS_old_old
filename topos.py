#! /usr/bin/env python3


# command-line parsing module
import argparse
import sys
import os


# ------- #
# Parsers #
# ------- #

# main parser from which we will create subparsers
parser = argparse.ArgumentParser(
    description = ('TOPOS: Tissue-of-Origin Predictor of Onco-Samples.\n' +  
                   'A robust SVC of the tissue of origin of' + 
                   'primaries, metastases, cell lines ' +
                   'and circulating tumor cells.')
)



# common parser for conversion and f ratio
parent_conversion_fratio = argparse.ArgumentParser(add_help = False)

# fratio, pvalue output file
parent_conversion_fratio.add_argument(
    '-o', '--output_file', 
    required = True
)


# common parser for tumor detection and TOO detection
parent_tumor_too = argparse.ArgumentParser(add_help = False)

# testing matrix (TPM)
parent_tumor_too.add_argument(
    '-tst', '--testing_exp',
    required = True
)

# gene list 
parent_tumor_too.add_argument(
    '-gl', '--gene_list_path')


# prediction directory
parent_tumor_too.add_argument(
    '-pd', '--prediction_directory',
    required = True
)


# ---------- #
# Subparsers #
# ---------- #

# subparser class
subparsers = parser.add_subparsers(
    title = 'subcommands',
    description = 'TOPOS modules', 
    dest = 'command',
    help = 'additional help',
    required = True
)


## Conversion ##

## create the subparser for the conversion command
parser_conversion = subparsers.add_parser('conversion', parents = [parent_conversion_fratio])

## add arguments

# user gene expression matrix
parser_conversion.add_argument(
    '-i', '--input_matrix',
    required = True,
    help = ('Path of gene expression file (.tsv).\n' + 
            'Rows are samples, columns are genes (Entrez ids).\n' + 
            'Expression values must be TPM.'
         )
)


## F ratio ##

## create the parser for the f-ratio computation
parser_f_ratio = subparsers.add_parser('f_ratio', parents = [parent_conversion_fratio])

## add arguments 

# expression matrix representing single-cell group
parser_f_ratio.add_argument(
    '-s', '--single_cell',
    default = './required_data/f_ratio/CTC-pooled_BRCA_tpm.tsv',
    help = ''
)


# expression matrix representing bulk group
parser_f_ratio.add_argument(
    '-b', '--bulk',
    default = './required_data/f_ratio/TCGA-BRCA_from_training_tpm.tsv',
    help = ''
)




## Tumor detection ##

## create the parser for the tumor_prediction command
parser_tumor_prediction = subparsers.add_parser(
    'tumor_prediction', 
    parents = [parent_tumor_too])


## TOO detection ##

# create the parser for the too_prediction command
parser_too_prediction = subparsers.add_parser(
    'too_prediction',
    parents = [parent_tumor_too])


# return some data from the options specified
args = parser.parse_args()
# print(args)



# ---------------- #
# Run TOPOS module #
# ---------------- #

# add path-with-module to python path at runtime
sys.path.append('./functions')


if args.command == 'conversion':
    
    print('\n')
    print('You are running TOPOS in\n')
    print(' +++++++++++++++++++\n', 
          '+ Conversion mode +\n', 
          '+++++++++++++++++++ ')
    print('\n')
    
    # import conversion function
    from conversion import conversion
    
    print('... Conversion to TPM starts ...\n')
    
    # convert
    conversion(
        testing_exp_path = args.input_matrix, 
        converted_exp_path = args.output_file
    )
    
    print('... Conversion to TPM ends ...\n')
    
    
elif args.command == 'f_ratio':
    
    print('\n')
    print('You are running TOPOS in\n')
    print(' ++++++++++++++++ \n', 
          '+ F ratio mode +\n', 
          '++++++++++++++++ ')
    print('\n')
    
    # import fratio comparison function
    from f_ratio import fratio_comparison
    
    print('... F-ratio computation starts ...\n')
    
    # compute f-ratio
    fratio_comparison(
        sc_exp_path = args.single_cell,
        bulk_exp_path = args.bulk,
        output_path = args.output_file
    )
    
    print('... F-ratio computation ends ...\n')
    
    
elif args.command == 'tumor_prediction':
    
    print('\n')
    print('You are running TOPOS in\n')
    print(' +++++++++++++++++++++++++\n', 
          '+ Tumor prediction mode +\n', 
          '+++++++++++++++++++++++++')
    print('\n')
    
    
    ## import functions
    from training import train
    from normalization import normalize
    from prediction import predict
    
    ## import packages
    import pandas as pd
    import numpy as np
    
    ## import data
    
    print('... Importing required data ...\n\n')
    
    # tumor prediction training matrix
    training_tp = pd.read_pickle('./required_data/tumor_prediction/training_tumor.pkl') 
        
    # tumor prediction training labels
    training_labels_tp = pd.read_pickle('./required_data/tumor_prediction/labels_training_tumor.pkl')
    
    # TOO prediction training matrix
    training_too = pd.read_pickle('./required_data/too_prediction/training_too.pkl')
    
    # testing matrix features
    testing_features = pd.read_table(
        args.testing_exp, 
        index_col = 0).columns.to_numpy()
    
    
    print('... Training tumor detection model starts ...\n')
    
    # encoder and classifier for tumor detection
    encdr, clf = train(
        training_exp = training_tp,
        training_labels = training_labels_tp,
        testing_features = testing_features,
        gene_list_path = args.gene_list_path
    )
    
    print('... Training tumor detection model ends ...\n\n')
    
    print('... Normalization of testing dataset starts ...\n')
    
    # normalize testing dataset on too training matrix
    testing_sw_fw = normalize(
        training_exp = training_too, 
        testing_exp_path = args.testing_exp, 
        gene_list_path = args.gene_list_path
    )
    
    print('... Normalization of testing dataset ends ...\n\n')
    
    print('... Tumor vs Non-tumor prediction starts ...\n')
    
    
    # prediction file
    prediction_file = os.path.join(
        args.prediction_directory, 
        ('P_tumor-non-tumor_') + str(testing_sw_fw.shape[1]) + '-genes.tsv'
    )
    
    # tumor detection predictions
    predict(
        testing_nrmlz = testing_sw_fw,
        clf = clf,
        encdr = encdr, 
        prediction_file = prediction_file
    )
    
    print('... Tumor vs Non-tumor prediction ends ...\n\n')
    
    
else: 
        
    print('\n')
    print('You are running TOPOS in\n')
    print(' ++++++++++++++++++++++\n', 
          '+ TOO detection mode +\n', 
          '++++++++++++++++++++++')
    print('\n')
    
    
    ## import functions
    from training import train
    from normalization import normalize
    from prediction import predict
    
    ## import packages
    import pandas as pd
    import numpy as np
    
    
    ## import data
    
    print('... Importing required data ...\n\n')
    
    # TOO prediction training matrix
    training_too = pd.read_pickle('./required_data/too_prediction/training_too.pkl')
    
    # TOO prediction training labels
    training_labels_too = pd.read_pickle('./required_data/too_prediction/labels_training_too.pkl')
    
    # testing matrix features
    testing_features = pd.read_table(
        args.testing_exp, 
        index_col = 0).columns.to_numpy()
    
    
    print('... Training TOO detection model starts ...\n')
    
    # encoder and classifier for tumor detection
    encdr, clf = train(
        training_exp = training_too,
        training_labels = training_labels_too, 
        testing_features = testing_features,
        gene_list_path = args.gene_list_path
    )
    
    print('... Training TOO detection model ends ...\n\n')
    
    print('... Normalization of testing dataset starts ...\n')
    
    # normalize testing dataset on too training matrix
    testing_sw_fw = normalize(
        training_exp = training_too, 
        testing_exp_path = args.testing_exp, 
        gene_list_path = args.gene_list_path
    )
    
    print('... Normalization of testing dataset ends ...\n\n')
    
    print('... TOO prediction starts ...\n')
    
    # prediction file
    prediction_file = os.path.join(
        args.prediction_directory, 
        ('P_TOO_') + str(testing_sw_fw.shape[1]) + '-genes.tsv'
    )
    
    # predict TOO
    predict(
        testing_nrmlz = testing_sw_fw,
        clf = clf,
        encdr = encdr, 
        prediction_file = prediction_file
    )
    
    print('... TOO prediction ends ...\n\n')
