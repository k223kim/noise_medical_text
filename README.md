# noise_medical_text

## Description

This project aims to generate noise to medical text dataset (e.g. MIMIC dataset) which are realistic enough to resemble radiologists' mistakes.

By adding noise, this new dataset with noise, can be used to train models to identify errors in medical documents. 

## Input

Input should be a json file (MIMIC-like format). 

## Output

Output will generate a new json file with added noise.

## Noise

Following errors are the noises that can be created with `python main_json.py --input=/path/to/input/`.

### Unit error

```
cm -> mm
mm -> cm
```

### Ajective error

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
