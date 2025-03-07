# Code for experiments conducted in the paper 'FoodSEM: Large Language Model Specialized in Food Named-Entity Linking' #

## Also checkout the trained model available on HuggingFace: huggingface.co/Anonymous-pre-publication/FoodSEM-LLM
## Installation, documentation ##

Published results were produced in Python 3.12 programming environment on AlmaLinux 8.10 (Cerulean Leopard) operating system. Instructions for installation assume the usage of PyPI package manager and availability of CUDA (we use version 12.8).<br/>


Clone the project from the repository.<br/>

Install dependencies if needed: pip install -r requirements.txt

### To reproduce the results published in the paper, run the code in the command line using following commands: ###

Data preprocessing - split the NEL and NER datasets into 5 train and test fold and make it appropriate to feed into language model:<br/>

```
python preprocess.py
```

The script creates two folders (by default 'train_sets_ner_nel' and 'test_sets_ner_nel') containing the train and test datasets for 5 folds. <br/>

Train and test 5 language models (one for each fold) on five folds:<br/>

```
python train_and_test.py
```

The script trains and saves the models and the models' outputs on the test sets in the results folder by default.<br/>

To apply the model on the new data, run the example apply script:<br/>

```
python apply.py
```

The script by default downloads the trained FoodSEM model from the Huggingface library.<br/>

Additionally, we offer script that we used for our baseline zero-shot and few-shot experiments:<br/>

```
python test_incontext.py
```








