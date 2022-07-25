TOPOS: Tissue-of-Origin Predictor of Onco-Samples
=================================================

A versatile machine-learning classifier based on SVMs to predict the tissue of origin (TOO) of primary, metastasis, cell line and circulating tumor cells (CTCs) samples.


Get TOPOS ready
---------------

You need to have Conda installed as a prerequisite.

1. Download TOPOS repository: `git clone https://github.com/DanCag/TOPOS`
2. Download TOPOS required files from
3. Move files into TOPOS folder
4. Go inside TOPOS directory: `cd TOPOS`
5. Extract each compressed archive `required_data.tar.gz`, `playground.tar.gz`, `example`:

```
tar xvf <compressed archive>
```
(you should see new directories with compressed archives' names after doing this)

6. Create the conda environment: `conda env create -f ./topos.yml`
7. Activate the environment `conda activate TOPOS`



Data
----
* `required_data` contains all necessary files for running TOPOS commands (such as the training matrixes)
* `playground` contains all the datasets on which we predict TOO in the study
* `example` is a folder user can use to run some tests

Usage
-----


The tool comes with three commands:

- `conversion` allows user to convert gene expression file from RPKM/FPKM to TPM

- `f_ratio` allows user to compute ANOVA F-ratio by comparing gene expression of each feature in single-cell and bulk experiment. F-ratio provides an estimate of divergence of gene expression between the groups compared. The command returns a table with F and p value for each gene. The user can then decide to pick only genes with close expression between the two groups for training and testing the classifiers.

- `tumor_prediction` trains a SVM to distinguish between tumor and non-tumor cells and make predictions on user gene expression dataset.

- `too_prediction` trains a SVM to distinguish between 15 different tissues of origin (TOOs) and make prediction on user expression dataset.



### Example of conversion

```
./topos.py conversion -i ./example/conversion/input/PDX-nature_fpkm.tsv -o ./example/conversion/output/PDX-nature_tpm.tsv 
```

**Required parameters**:

* `-i`, `--input_matrix`<br>
path of user's gene expression matrix. Gene expression matrix must be in the following format


| | | | | |
| :----:  | :----: | :----: | :----: | :----: |
|         | gene_1 | gene_2 | ...    | gene_n | 
| sample1 |
| sample2 |
| ...     | 
| samplen |

The file is tab-separated. Rows are samples and columns are genes (named with Entrez gene ids).<br>
Columns and samples must be named, so there will be a column and a row index.<br>

You can find the input files used in the study in the folder `./playground/datasets/`.
 
* `-o`, `--output_file`<br>
path where to write the converted expression matrix file (tab-separated).

*Runtime*: ~ 0.3 minute



### Example of F-ratio computation

```
./topos.py f_ratio -o ./example/f_ratio/output/f_ratio.tsv

```

**Required parameters**

- `-o`, `--output_file`<br>
path where to write the tab-separated file (tsv) with F and p values.<br>

**Optional parameters**
 
- `-s`, `--single_cell`<br>
path of single-cell gene expression matrix to use for the comparison.<br> 
Default is a gene expression matrix (TPM) with pooled breast CTCs.

- `-b`, `--bulk`<br>
path of bulk gene expression matrix path to use for the comparison.<br>
Default is a gene expression matrix (TPM) with TCGA-BRCA samples extracted from training matrix.<br>

Default matrixes are available in ./required_data/f_ratio under the name _CTC-pooled_BRCA_tpm.tsv_ and _TCGA-BRCA\_from_training_tpm.tsv_ respectively. These are the matrixes used in the study to compute F-ratio.

*Runtime*: ~ 4 hours (default single-cell matrix has 339 cells, default bulk matrix has 662 samples, genes in common are 14112)



### Example of tumor prediction

```
./topos.py tumor_prediction -tst ./playground/datasets/breast-GSE109761_tpm.tsv -gl ./required_data/less_divergent_genes.txt -pd ./example/tumor_prediction/output
```

**Required parameters**

- `-tst`, `--testing_exp`<br>
path of user's testing expression matrix

- `-pd`, `--prediction_directory`<br>
path of prediction directory where to store prediction file


**Optional parameter**

- `-gl`, `--gene_list`<br>
path of gene list file. The file contains genes (entrez gene ids) to use for training and testing.<br>
If not provided, TOPOS will use the overlap between training and testing matrixes' features.

*Runtime*: ~ 0.4 minute



### Example of TOO prediction
```
./topos.py too_prediction -tst ./playground/datasets/breast-GSE109761_tpm.tsv -gl ./required_data/less_divergent_genes.txt -pd ./example/too_prediction/output

```

**Required parameters**

- `-tst`, `--testing_exp`<br>
path of user's testing expression matrix

- `-pd`, `--prediction_directory`<br>
path of prediction directory where to store prediction file


**Optional parameter**

- `-gl`, `--gene_list`<br>
path of gene list file. The file contains genes (entrez gene ids) to use for training and testing.<br>
If not provided, TOPOS will use the overlap between training and testing matrixes features.

*Runtime*: ~ 1 minute


### Runtime tests
Runtimes are estimated on the following machine:

| | |
| :----: | :----: |
| **OS**     | Ubuntu 20.04.4 LTS |
| **Memory** | 5.5 Gib     |
| **Processor** | Intel® Core™ i5-8500T CPU @ 2.10GHz × 6 |

























# Markdown syntax guide

## Headers

# This is a Heading h1
## This is a Heading h2 
###### This is a Heading h6

## Emphasis

*This text will be italic*  
_This will also be italic_

**This text will be bold**  
__This will also be bold__

_You **can** combine them_

## Lists

### Unordered

* Item 1
* Item 2
* Item 2a
* Item 2b

### Ordered

1. Item 1
1. Item 2
1. Item 3
  1. Item 3a
  1. Item 3b

## Images

![This is a alt text.](/image/sample.png "This is a sample image.")

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
>
>> Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.

## Tables

| Left columns  | Right columns |
| ------------- |:-------------:|
| left foo      | right foo     |
| left bar      | right bar     |
| left baz      | right baz     |

## Blocks of code

```
let message = 'Hello world';
alert(message);
```

## Inline code

This web site is using `markedjs/marked`.
