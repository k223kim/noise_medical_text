# noise_medical_text

## Description

This project aims to generate noise to medical text dataset (e.g. MIMIC dataset) which are realistic enough to resemble radiologists' mistakes.

By adding noise, this new dataset with noise, can be used to train models to identify errors in medical documents. 

## Input

Input should be a json file (MIMIC-like format). 

## Output

Output will generate a new json file with added noise.

## Noise

There are three types of realistic errors:

### 1. Perception Error

When an existing lesion is missed in the document.

### 2. Interpretation Error

When the described lesion is incorrect (incorrectly labeled).

### 3. Writing Error

#### 3.1. Unit Error
```
cm -> mm
mm -> cm
```
#### 3.2. Adjective Error
```
left -> right
right -> left
upper -> lower
lower -> upper
high -> low
low -> high
partially -> fully
fully -> partially
big -> small
small -> big  
```
Following errors are the noises that can be created with `python main_json.py --input=/path/to/input/`.
