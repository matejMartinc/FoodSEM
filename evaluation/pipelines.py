import csv

from modifiers import NelBaseModifier, FoodOnNelExtendedModifier, HansardNelModifier, SaHansardNelModifier, \
    SnomedNelExtendedModifier
from entities import NelDataset


class Writer:
    @staticmethod
    def write(save_file: str, append: bool, questions: list):
        if append:
            with open(save_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                for question in questions:
                    writer.writerow(question)
        else:
            with open(save_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                for question in questions:
                    writer.writerow(question)


class NerNelPipeline:
    @staticmethod
    def continue_processing(row: dict, ontology: str):
        if ontology in row['Original prompt'].lower():
            return True
        else:
            return False

    @staticmethod
    def read_test_instance(row: dict):
        original_prompt = row['Original prompt'].split(sep='</div>')[0].strip()
        original_prompt = original_prompt[:-1] if original_prompt.endswith('.') else original_prompt
        true_prompt = row['True prompt']
        actual_answer = row['Answer']
        answer = row['Answer']
        true_answer = row['True']
        return [original_prompt, true_prompt, actual_answer, answer, true_answer]

    def run(self, dataset_files, input_test_file, data, ontology, clean=False, modifier='base'):
        dataset = NelDataset()
        writer = Writer()
        if ontology == 'foodon':
            if modifier == 'base':
                cleaner = NelBaseModifier()
            elif modifier == 'extended':
                cleaner = FoodOnNelExtendedModifier()
        elif ontology == 'snomed':
            if modifier == 'base':
                cleaner = NelBaseModifier()
            elif modifier == 'extended':
                cleaner = SnomedNelExtendedModifier()
        else:
            if data == 'fcd':
                cleaner = HansardNelModifier()
            else:
                cleaner = SaHansardNelModifier()

        for dataset_file in dataset_files:
            with (open(dataset_file, encoding='utf-8') as f):
                reader = csv.DictReader(f, fieldnames=['prompt'], delimiter='\n')
                for row in reader:
                    if not row['prompt'].replace(' ', ''):
                        continue
                    prompts = row['prompt'].split(sep='[INST]')
                    [_, original_prompt] = prompts[1].split(sep='[/INST]')
                    for nel_prompt in prompts[2:]:
                        if ontology.lower() in nel_prompt.lower():
                            [_, true_answer] = nel_prompt.split(sep='[/INST]')
                            dataset.add_labels(prompt=original_prompt, answer=true_answer)

        with (open(input_test_file, encoding='utf-8') as f):
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                continue_processing_ = self.continue_processing(row=row, ontology=ontology)
                if not continue_processing_:
                    continue

                [original_prompt, true_prompt, actual_answer, answer, true_answer] = self.read_test_instance(row=row)

                if clean:
                    answer = cleaner.clean(text=answer)

                dataset.add_test_instance(
                    original_prompt=original_prompt,
                    true_prompt=true_prompt,
                    true_answer=true_answer,
                    predicted_answer=answer,
                    actual_predicted_answer=actual_answer
                )

        dataset.fit_labels()

        summary_result = dataset.print()
        writer.write(input_test_file.replace('.tsv', f'_{modifier}_{ontology}_summary.csv'), False,
                          summary_result)


class NelPipeline:
    @staticmethod
    def run(dataset_files, input_test_file, ontology, clean=False, modifier='base'):
        dataset = NelDataset()
        writer = Writer()
        if ontology == 'foodon':
            if modifier == 'base':
                cleaner = NelBaseModifier()
            elif modifier == 'extended':
                cleaner = FoodOnNelExtendedModifier()
        elif ontology == 'snomed':
            if modifier == 'base':
                cleaner = NelBaseModifier()
            elif modifier == 'extended':
                cleaner = SnomedNelExtendedModifier()
        else:
            cleaner = HansardNelModifier()

        for dataset_file in dataset_files:
            with (open(dataset_file, encoding='utf-8') as f):
                reader = csv.DictReader(f, fieldnames=['prompt'], delimiter='\n')
                for row in reader:
                    if not row['prompt'].replace(' ', ''):
                        continue
                    prompts = row['prompt'].split(sep='[INST]')
                    [_, original_prompt] = prompts[1].split(sep='[/INST]')
                    for nel_prompt in prompts[2:]:
                        if ontology.lower() in nel_prompt.lower():
                            [_, true_answer] = nel_prompt.split(sep='[/INST]')
                            dataset.add_labels(prompt=original_prompt, answer=true_answer)

        with (open(input_test_file, encoding='utf-8') as f):
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                original_prompt = row['Original prompt']
                true_prompt = row['True prompt']
                actual_answer = row['Answer']
                answer = row['Answer']
                true_answer = row['True']

                if clean:
                    answer = cleaner.clean(text=answer)

                dataset.add_test_instance(
                    original_prompt=original_prompt,
                    true_prompt=true_prompt,
                    true_answer=true_answer,
                    predicted_answer=answer,
                    actual_predicted_answer=actual_answer
                )

        dataset.fit_labels()

        summary_result = dataset.print()
        writer.write(input_test_file.replace('.tsv', f'_{modifier}_{ontology}_summary.csv'), False, summary_result)


if __name__ == '__main__':
    nel_pipeline = NerNelPipeline()

    dataset_files = [r'path\to\cafeteriafcd\dataset', r'path\to\cafeteriasa\dataset']
    input_file = r'path\to\crossvalidation\file'
    nel_pipeline.run(dataset_files=dataset_files, input_test_file=input_file, data='fcd', ontology='foodon', clean=True)

    pipeline = NelPipeline()

    dataset_files = [r'path\to\cafeteriafcd\dataset', r'path\to\cafeteriasa\dataset']
    input_file = r'path\to\crossvalidation\file'
    pipeline.run(dataset_files=dataset_files, input_test_file=input_file, ontology='foodon', clean=True)
