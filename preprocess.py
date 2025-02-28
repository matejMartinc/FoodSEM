import pandas as pd
from datasets import load_dataset
import random
import os
from sklearn.model_selection import KFold


TRAIN_SET_PATH = 'train_sets_ner_nel'
TEST_SET_PATH = 'test_sets_ner_nel'

def cv_split(df, output_name):
    kf = KFold(n_splits=5, shuffle=True, random_state=123)
    for idx, split in  enumerate (kf.split(df)):
        train_df = df.iloc[split[0]]
        test_df = df.iloc[split[1]]
        if not os.path.exists(TRAIN_SET_PATH + '/' + f'split_{idx}/'):
            os.makedirs(TRAIN_SET_PATH + '/' + f'split_{idx}/')
        if not os.path.exists(TEST_SET_PATH + '/' + f'split_{idx}/'):
            os.makedirs(TEST_SET_PATH + '/' + f'split_{idx}/')
        train_df.to_csv(TRAIN_SET_PATH + '/' + f'split_{idx}/' + output_name + '.tsv', encoding='utf8', index=False, sep='\t')
        test_df.to_csv(TEST_SET_PATH + '/' + f'split_{idx}/' + output_name + '.tsv', encoding='utf8', index=False, sep='\t')


def preprocess_ner():
    datasets = ['data/NER and NEL/FCD_new_mistral.txt',
                'data/NER and NEL/SA_mistral_new.txt']
    for dt_path in datasets:
        output_name = (dt_path.split('/')[1] + '_' + dt_path.split('/')[2]).replace(' ', '_').lower().split('.')[0]
        kf = KFold(n_splits=5, shuffle=True, random_state=123)
        with open(dt_path, 'r', encoding='utf8') as f:
            df = pd.DataFrame(f.readlines(), columns=['text'])
            for cv_idx, split in enumerate(kf.split(df)):
                train_df = df.iloc[split[0]]
                test_df = df.iloc[split[1]]
                if not os.path.exists(TRAIN_SET_PATH + '/' + f'split_{cv_idx}/'):
                    os.makedirs(TRAIN_SET_PATH + '/' + f'split_{cv_idx}/')
                if not os.path.exists(TEST_SET_PATH + '/' + f'split_{cv_idx}/'):
                    os.makedirs(TEST_SET_PATH + '/' + f'split_{cv_idx}/')

                counter = 0
                train_dataset = []
                for line in train_df['text'].tolist():
                    if len(line.strip()) > 0:
                        chunks = line.split('[INST]')
                        counter += 1
                        prev_output = ''
                        for idx, chunk in enumerate(chunks):
                            if len(chunk.strip()) > 0:
                                instruction, output = chunk.strip().split('[/INST]')
                                if idx > 1:
                                    instruction = prev_output + ' </div> ' + instruction
                                train_dataset.append((instruction.strip(), output.strip()))
                                if idx == 1:
                                    prev_output = output
                test_dataset = []
                for line in test_df['text'].tolist():
                    if len(line.strip()) > 0:
                        chunks = line.split('[INST]')
                        counter += 1
                        prev_output = ''
                        for idx, chunk in enumerate(chunks):
                            if len(chunk.strip()) > 0:
                                instruction, output = chunk.strip().split('[/INST]')
                                if idx > 1:
                                    instruction = prev_output + ' </div> ' + instruction
                                test_dataset.append((instruction.strip(), output.strip()))
                                if idx == 1:
                                    prev_output = output
                train_df = pd.DataFrame(train_dataset, columns=['instruction', 'output'])
                train_df = train_df.sample(frac=1, random_state=123).reset_index(drop=True)
                train_df.to_csv(TRAIN_SET_PATH + '/' + f'split_{cv_idx}/' + output_name + '.tsv', encoding='utf8', index=False, sep='\t')
                test_df = pd.DataFrame(test_dataset, columns=['instruction', 'output'])
                test_df.to_csv(TEST_SET_PATH + '/' + f'split_{cv_idx}/' + output_name + '.tsv', encoding='utf8', index=False, sep='\t')


def preprocess_nel_bootstrap():
    datasets = ['data/NEL bootstrap samples/FCD_mistral_foodon.txt',
                'data/NEL bootstrap samples/FCD_mistral_hansard.txt',
                'data/NEL bootstrap samples/FCD_mistral_snomed_ct.txt']

    for ds in datasets:
        dataset = []
        output_name = (ds.split('/')[1] + '_' + ds.split('/')[2]).replace(' ', '_').lower().split('.')[0]
        with open(ds, 'r', encoding='utf8') as f:
            docs = f.readlines()
            for line in docs:
                if len(line.strip()) > 0:
                    line = line.replace('[INST]', '')
                    instruction, output = line.strip().split('[/INST]')
                    dataset.append((instruction.replace(' ?', '?').strip(), output.strip()))
        df = pd.DataFrame(dataset, columns=['instruction', 'output'])
        cv_split(df, output_name)


if __name__ == '__main__':
    preprocess_ner()
    preprocess_nel_bootstrap()









