# learnX.ai

## Introduction
## Goals
## Contributors
The contributor of the project is Amir Bhattarai. [www.linkedin.com/in/amir-bhattarai-1170511ab][Linkedin Profile]
## Project Architecture


# Status
## Known Issue
## High Level Next Steps


# Usage
## Installation
To begin this project, use the included `Makefile`

#### Creating Virtual Environment

This package is built using `python-3.8`. 
We recommend creating a virtual environment and using a matching version to ensure compatibility.

#### pre-commit

`pre-commit` will automatically format and lint your code. You can install using this by using
`make use-pre-commit`. It will take effect on your next `git commit`

#### pip-tools

The method of managing dependencies in this package is using `pip-tools`. To begin, run `make use-pip-tools` to install. 

Then when adding a new package requirement, update the `requirements.in` file with 
the package name. You can include a specific version if desired but it is not necessary. 

To install and use the new dependency you can run `make deps-install` or equivalently `make`

If you have other packages installed in the environment that are no longer needed, you can you `make deps-sync` to ensure that your current development environment matches the `requirements` files. 

## Usage Instructions


# Data Source
The data is available at huggingface datasets and can be accessed using the link provided below.
[https://huggingface.co/datasets/rajpurkar/squad][Dataset Link]
## Code Structure
## Artifacts Location
The artifacts are stored in the drive link given below. Inside this there is a folder named checkpoints which contains the last checkpoint when training ends. There remain files which are named last-t5b.ckpt, last-t5s.ckpt which corresponds to the t5-base model and t5-small model fine-tuned for question and/or generation tasks respectively. Similarly, the last-tc.ckpt corresponds to the distilbert-base-uncased model fine-tuned for token classification. There also remain two other folders named squad and squad-iob respectively. The squad folder contains the tokenized version of already available squad dataset customized for question and/or generation task. likewise, the squad-iob is prepared for token classification but not tokenized.
[https://drive.google.com/drive/folders/1ZsNwsvuFRQwiP1N0hlUJ4pP6PmuKw2C9?dmr=1&ec=wgc-drive-hero-goto][Drive Link]
# Results
## Metrics Used
## Evaluation Results
