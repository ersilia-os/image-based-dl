# Image-based chemical property descriptors for antimalarial drug screening

Repository of the Final Thesis of the Master in Fundamental Principles of Data Science (University of Barcelona).

_Author: Núria Camí_

<!-- Exploitation of the Medicines for Malaria Venture (MMV) dataset on the activity of putative antimalarial compounds in asexual blood stages of the Plasmodium Falciparum parasite. Usage of the [MolMap](https://github.com/shenwanxiang/bidd-molmap) library as a DL model for predicting the activity of the molecules against the pathogen that causes Malaria.
 -->

## Installation

1. Install the necessary pip and conda packages from my environment:
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

<!-- - data: contains the datasets used for the different implementations.
- deliverables: contains the report and the slides presentation for the defense.
- files: contains the files saved on disk generated for the different implementations.
- notebooks: contains all the scripts coded for developing the project.
- src: source files containing logic classes.
- tools: [bidd-molmap](https://github.com/shenwanxiang/bidd-molmap) cloned repository with minor modifications in order to fit our problem. -->

## Learn more

The [Ersilia Open Source Initiative](https://ersilia.io) is on a mission to strenghten research capacity in low income countries. Please reach out to us if you want to contribute: [hello@ersilia.io]()

