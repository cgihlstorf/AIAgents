import os






if __name__ == "__main__":

    output_dir = "output_files"

    #MODEL_NAME = "allenai/OLMo-2-0425-1B-SFT" 
    MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
    model_name_short = MODEL_NAME.split("/")[1]

    compute_type = "GPU" #GPU or cpu

    quantization = "full" #full, 4bit, or 8bit

    file_substring = f'{model_name_short}_results_{quantization}_{compute_type}_'

    found_files = []

    for root, dirs, files in os.walk(output_dir):

        for file_name in files:
            if file_substring in file_name:
                found_files.append(file_name)

    assert len(found_files) == 1 #we don't want 2 of the same file (same settings, run at different times)

    file_path = f'{output_dir}/' + found_files[0]

    print(file_path)

    #code an option to output a list of all the ground truth answers mapped to the model answers for a heatmap
    #rerun original models with this
    #open this file, get ground truth and model answers
    #make a heatmap


    pass