# Entity Resolution Pipeline – Dragonfly Project

This project performs entity resolution (record linkage) across two datasets by cleaning, transforming, and comparing product records using fuzzy string matching. The final output is a unified product catalogue.

---

## Overview

This pipeline links records from two product sources by:

1. Preprocessing datasets
2. Looking for missing values and analysing their type
3. Performing deduplication with blocking, using python package recordlinkage

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/irene-crepax/dragonfly-entity-resolution.git
cd dragonfly-entity-resolution
```
### 2. Set up a conda environment and install requirements
```bash
conda create -n dragonfly
conda activate dragonfly 
conda install conda-forge::pandas
conda install conda-forge::spacy
conda install conda-forge::recordlinkage

```

## Execute 
Modify each python file for your inputs.
### 1. preprocessing_step.py:

requires paths to your csv files

### 2. missing_values_analysis.py:
if after the previous step, you find a significant number missing values with statistically significant correlations, run this script to decide how to proceed. 

### 3. er.py:
requires file paths, blocking variable names, and comparison variable names.