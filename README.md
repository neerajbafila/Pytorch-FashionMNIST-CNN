# To create env

# STEPS

## Step 01 - Create a repository by using template repository
## step 02 - Clone the new repository
## step 03 - Create a conda environment after opening the repository in VSCODE
```
conda create --prefix ./env python=3.8 -y
```
## activate environment
```
conda activate ./env
```
### or
```
source activate ./env
```

## STEP 04- install the requirements
```
pip install -r requirements.txt
```

## step 05- install pytorch with cuda

```
conda install pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia
```
step 06- install setup.py
```
pip install -e .
```

## to run ml project from local

```
mlflow run . --env-manager local
```