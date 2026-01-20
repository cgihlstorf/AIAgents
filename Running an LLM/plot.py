import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json


def make_plots(file_paths:list, output_file_name:str):

    answer_matrix = [[0 for _ in file_paths] for _ in file_paths] #make an nxn matrix for a heatmap
    heatmap_dict = {}

    models = []
    subjects = []
    accs = []

    for file_path in file_paths:

        file_path_items = file_path.replace("output_files/", "").split("_")
        model_name = file_path_items[0]
        quant_config = file_path_items[2]
        architecture = file_path_items[3]

        file = open(file_path, 'r')
        file_string = file.read()
        file_dict = json.loads(file_string)

        subject_results = file_dict["subject_results"]
        
        for subject_dict in subject_results:

            subject = subject_dict["subject"]
            accuracy = subject_dict["accuracy"]
            ground_truth_answers = subject_dict["ground_truth_answers"]
            model_answers = subject_dict["model_answers"]

            models.append(model_name)
            subjects.append(subject)
            accs.append(accuracy)

            if subject not in heatmap_dict.keys():
                heatmap_dict[subject] = {}

            heatmap_dict[subject][model_name] = model_answers #TODO check



    for subject in heatmap_dict.keys():

        subject_dict = heatmap_dict[subject]
        heatmap_models = []

        for i in range(len(list(subject_dict.keys()))):

            model_1 = list(subject_dict.keys())[i]
            m1_answers = subject_dict[model_1]
            heatmap_models.append(model_1)

            for j in range(len(list(subject_dict.keys()))):
                
                model_2 = list(subject_dict.keys())[j]
                m2_answers = subject_dict[model_2]

                overlap = compute_overlap(m1_answers, m2_answers)
                answer_matrix[i][j] = overlap

        plt.figure(figsize=(14, 7))
        heatmap = sns.heatmap(np.array(answer_matrix), xticklabels=heatmap_models, yticklabels=heatmap_models, annot=True)
        plt.title(f'{subject} {output_file_name}')
        plt.savefig(f'figures/{output_file_name}_{subject}_heatmap.pdf')

    
    
    accuracy_df = pd.DataFrame({
        "Model" : models,
        "Subject" : subjects,
        "Accuracy" : accs,
    })


    plt.figure(figsize=(10, 8))
    acc_barplot = sns.barplot(accuracy_df, x="Model", y="Accuracy", hue="Subject")
    plt.title(f'MMLU Results {output_file_name}')
    plt.savefig(f'figures/{output_file_name}_accuracies.pdf')


def choose_files(output_dir:str, by_model:bool=False, model:str=None, by_quant:bool=False, quant:str=None, by_architecture:bool=False, architecture:str=None):

        model_specs = []

        if by_model:
            assert model != None
            model_specs.append(model)
        if by_quant:
            assert quant != None
            model_specs.append(quant)
        if by_architecture:
            assert architecture != None
            model_specs.append(architecture)

        model_substr = "_" + "_".join(model_specs) + "_"

        found_files = []

        for root, dirs, files in os.walk(output_dir):
            for file_name in files:
                if model_substr in file_name:
                    found_files.append(f'{output_dir}/' + file_name)

        return found_files, model_substr[1:-1]

        
def compute_overlap(lst1, lst2):

    assert len(lst1) == len(lst2)
    
    total_items = len(lst1)
    matching_items = 0
    
    for i1, i2 in zip(lst1, lst2):
        if i1 == i2:
            matching_items += 1

    return matching_items / total_items







if __name__ == "__main__":

    output_dir = "output_files"

    file_paths, output_file_name = choose_files(output_dir, by_quant=True, quant="full", by_architecture=True, architecture="mps")

    make_plots(file_paths, output_file_name)