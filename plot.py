import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json


def make_plots(file_paths:list, output_file_name:str):

    answer_matrix = [[0 for _ in file_paths] for _ in file_paths] #make an nxn matrix for a heatmap

    models = []
    subjects = []
    accs = []

    for file_path in file_paths:

        file_path_items = file_path.replace("output_files/", "").split("_")
        model_name = file_path_items[0]
        quant_config = file_path_items[2]
        architecture = file_path_items[3]
        file_name_short = f'{model_name}_{quant_config}_{architecture}'

        file = open(file_path, 'r')
        file_string = file.read()
        file_dict = json.loads(file_string)

        subject_results = file_dict["subject_results"]
        
        for subject_dict in subject_results:

            subject = subject_dict["subject"]
            accuracy = subject_dict["accuracy"]
            ground_truth_answers = subject_dict["ground_truth_answers"]
            model_answers = subject_dict["model_answers"]

            models.append(file_name_short.replace(f'_{output_file_name}', ""))
            subjects.append(subject)
            accs.append(accuracy)

    
    accuracy_df = pd.DataFrame({
        "Model" : models,
        "Subject" : subjects,
        "Accuracy" : accs,
    })

    print(accuracy_df)


    plt.figure()
    acc_barplot = sns.barplot(accuracy_df, x="Model", y="Accuracy", hue="Subject")
    plt.title(f'MMLU Results {output_file_name}')
    plt.savefig(f'figures/{output_file_name}.png')

    #TODO correlations for each model


def choose_files(by_model:bool=False, model:str=None, by_quant:bool=False, quant:str=None, by_architecture:bool=False, architecture:str=None):

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
        





if __name__ == "__main__":

    output_dir = "output_files"

    file_paths, output_file_name = choose_files(by_quant=True, quant="full", by_architecture=True, architecture="GPU")

    make_plots(file_paths, output_file_name)

    #open this file, get ground truth and model answers
    #make a heatmap