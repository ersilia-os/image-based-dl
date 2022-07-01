# Image-based chemical property descriptors for antimalarial drug screening

Repository of the Final Thesis of the Master in Fundamental Principles of Data Science (University of Barcelona).

_Author:_ Núria Camí.

_Supervisors:_ Miquel Duran-Frigola (Ersilia), Gemma Turon (Ersilia), Jordi Vitrià (UB).

## Introduction

This repository contains all code produced for the project, mainly focused on the implementation of the [MolMap](https://github.com/shenwanxiang/bidd-molmap) library as a Deep Learning model for predicting the activity (active/inactive) of experiments on chemical compounds. For simplicity, the code has been reproduced with a small dataset, although specific notebooks have been created so that it can be reproduced with large datasets. For full explanation, please refer to the [report document](report.pdf). 

## Installation

1. Install the necessary pip and conda packages from the project environment:
    - Download the ```environment.yml``` and create the environment from this file: ```conda env create -f environment.yml```
    - Activate the new environment: ```conda activate molmap```
    - Verify that the new environment was installed correctly: ```conda env list```

If you see 'molmap' on your environments list, you can proceed with the next step. 


2. Install [Griddify](https://github.com/ersilia-os/griddify):
```
git clone https://github.com/ersilia-os/griddify.git
cd griddify
pip install -e .
```

3. Install [Ondisk-xy](https://github.com/ersilia-os/ondisk-xy):
```
git clone https://github.com/ersilia-os/ondisk-xy.git
cd ondisk-xy
pip install -e .
```

4. If you want to manage the files (placed on folder 'files') as [Large File Storage (LFS)](https://git-lfs.github.com/), it may be advisable to install also LFS:

```
git lfs install
```

## Content

This repository includes the following directories:

- **data**: dataset available for reproducing the code:
    > CYP PubChem BioAssay CYP 1A2, 2C9, 2C19, 2D6, 3A4 inhibition, from  [Chembench](https://github.com/shenwanxiang/ChemBench/tree/master/src/chembench/data_and_index/CYP450).
- **files**: objects and models saved on disk.
- **notebooks**: Jupyter Notebooks, organized by datasets:
    - **CYP450**: baselines and MolMap implemented to a small dataset. 
    - **large_dataset***: notebooks for replicating MolMap implementation in a larger dataset. 
        > Random Forest and a basic CNN as a baselines, Ensemble and Generator approaches for MolMap.
    - **MNIST**: experiments performed to test the robustness of image construction of MolMap.
- **src**: source files containing logic classes.
- **tools**: [bidd-molmap](https://github.com/shenwanxiang/bidd-molmap) cloned repository including a new class [MultiClassEstimator_largedata](tools/bidd-molmap/molmap/model/model.py) that allows training the MolMapNet with generators. 

*_For simplicity, notebooks from both folders CYP450 and large_dataset have been tested with the same dataset (CYP PubChem BioAssay CYP 1A2, 2C9, 2C19, 2D6, 3A4 inhibition), although the large_dataset ones have been specially created for applying MolMap to larger datasets, as its name indicates._

And finally, the document for the [project report](report.pdf).

## Learn more

The [Ersilia Open Source Initiative](https://ersilia.io) is on a mission to strengthen research capacity in low income countries. Please reach out to us if you want to contribute: [hello@ersilia.io]()

