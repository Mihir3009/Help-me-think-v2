#!/usr/bin/env python3
import json
from os import listdir
from os.path import isfile, join

# read all the tasks and make sure that they're following the right pattern
tasks_path = 'tasks/'

expected_keys = [
    "Domain",
    "Task",
    "Prompt",
    "Instances",
    "Preset_link"
]

prompt_nested_keys = [
    "pre_question_prompt",
    "task_specific_prompt"
]

nested_keys = [
    "QApair",
    "Output"
]

nested_QApair_check = [
    "Question",
    "Answer"
]

with open("tasks/README.md", 'r') as readmef:
    task_readme_content = " ".join(readmef.readlines())
files = [f for f in listdir(tasks_path) if isfile(join(tasks_path, f))]
files.sort()

for file in files:
    if ".md" not in file:
        print(f" --> testing file: {file}")
        assert '.json' in file, 'the file does not seem to have a .json in it: ' + file
        file_path = tasks_path + file
        with open(file_path, 'r') as f:
            data = json.load(f)
            for key in expected_keys:
                assert key in data, f'did not find the key: {key}'

            assert len(data[
                           'Instances']) > 0, f"there must be at least one instance; currently you have {len(data['Instances'])} instances"
            assert len(data[
                           'Instances']) < 4, f"there must be at most three instances; currently you have {len(data['Instances'])} instances"

            assert type(data['Domain']) == str, f'Domain must be a string.'
            #assert type(data['Contributors']) == list, f'Contributors must be a list.'
            assert type(data['Task']) == str, f'Task must be a string.'
            assert type(data['Prompt']) == dict, f'Prompt must be a dictionary.'
            assert type(data['Instances']) == list, f'Instances must be a list.'
            assert type(data['Preset_link']) in [list, str], f'Preset link must be a list.'
            
            for key in prompt_nested_keys:
                assert key in data['Prompt'], f'did not find the key in prompt dictionary: {key}'
                
            for dict_ in data['Instances']:
                for key in dict_.keys():
                    assert key in nested_keys, f'did not find the key in Instances: {key}'
                for sub_dict_ in dict_:
                    for sub_key in sub_dict_.keys():
                        assert sub_key in nested_QApair_check, f'did not find the key in QA pair: {sub_key}'

            true_file = file.replace(".json", "")
            for char in true_file:
                if char.isupper():
                    raise Exception(f" * Looks like there is an uppercase letter in `{true_file}`. All letters should be lowercased.")

            if file in task_readme_content:
                raise Exception(f" * Looks like the .json file extension ending is present with the task name in `tasks/README.md` when it should just be `{true_file}`")

            if true_file not in task_readme_content:
                raise Exception(f' * Looks like the task name `{true_file}` is not included '
                                f'in the task file `tasks/README.md`')

print("Did not find any errors! ✅")
