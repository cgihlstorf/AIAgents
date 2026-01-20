# Running an LLM

## General Overview

For this assignment, I ran several language models on subsets of the `MMLU` benchmark on both my local laptop and Google Colab. I analyzed their performance and compared the overlap between their multiple-choice answers. For running locally, I chose to use `Llama-3.2 1B Instruct`, `OLMo-2 1B SFT`, and `Qwen-2.5 0.5B`. On Colab, I used three models plus three medium-sized models: `Llama-3.1 8B`, `OLMo-2 7B`, and `Qwen-2.5 7B`. Analyses of these results on both my local machine and Colab can be found below. 

I then tested `Llama-3.2 1B Instruct` as a chat agent on my local laptop. Using the code provided for the assignment as a starter, I modified it to limit the model's chat context to only the previous 10 rounds of conversation. I thenn instroduced a variable that determined whether the model has access to any context at all and had two conversations with it in each setting - with context and without context. I provide a qualitative analysis of these two conversations in question 2 of `Results - Local Laptop`. 

## Folder Guide

`chat_histories` contains files of the chats I had with the `Llama-3.2 1B Instruct` agent both with and without conversation history.

`figures` contains plots and graphs of the results of running models on `MMLU` on 10 subjects.

`output_files` contains the output files for each model run on 10 subjects on `MMLU`. No quantization was used for these experiments, but I did vary whether I used a CPU or a GPU.

`output_files_2_subjects` contains output files for models I ran on 2 subjects, testing on both CPU and GPU.

The `colab_link.txt` file contains the link to the Colab file I used to replicate some of these experiments. Figures and output files for the Colab experiment are in a separate folder entitled `hw1_outputs_colab`.


## Results - Local Laptop

1. **Run the code and create graphs of the results.  Can you see any patterns to the mistakes each model makes or do they appear random?  Do the all the models make mistakes on the same questions?**

Plots for models run on 10 subjects can be found in the `figures` folder. Results are for models run on GPUs with no quantization. I tested three models: `Llama-3.2 1B Instruct`, `OLMo-2 1B SFT`, and `Qwen-2.5 0.5B`. Overall, accuracy for all three models was highest on questions pertaining to US foreign polic and lowest on questions about professional accounting. This could be because the training data for the models contained more information related to US foreign policy, than professional accounting, which would make sense given that US foreign policy might be discussed in news articles and websites more frequently than professional accounting, which is a specific discipline. I also measure agreement between models using heatmaps, where the agreement between two models is calculated as the overlap between the answers they give on each question (ranging from 0.0 - 1.0). Astronomy, business ethics, nutrition, philosophy, and prehistory display similar performances across models. As displayed in the heatmaps, models displayed moderate overlap in their answers over all subjects, with some of the most agreement between models being in US foreign policy (agreement here ranges from 0.64 to 0.7). A very low overlap of 0.28 was observed between `OLMo` and `LLama` on professional accounting, and the overlaps for other models were moderate at best, suggesting that models both performed worse and had very different answers from one another on these questions, indicating potential randomness in their answers. 

2. Add a flag so that you can turn off the conversation history. Compare how the chat agent performs on a multi-turn conversation when the history is maintained and when it is not.

I added a variable that controls whether models save chat history or not. I used `Llama-3.2 1B Instruct` as the chat model. I chatted with the model once with keeping the conversation history (up to 10 turns) and once without keeping any conversation history at all. Logs from these conversations can be found in thr `chat_histories' folder. I began by asking the model for advice on studying more productively. When the chat history was saved, the model was able to keep track of my questions and relate its answers back to previous context quite easily. The model stayed on-topic (i.e., kept the conversation focused on studying) and kept bringing back study tips into the conversation even when my inputs were not specific questions. For example, I told the model "I usually study at my desk" and it proceeded to give me tips on how to organize my desk to make studying the most productive. When I thanked the model at the end of the conversation, the model wished me luck with my studies, demonstrating that it remembered the previous turns of our conversation.

When I turned off chat history, my conversation with the model went very differently. I began with the same question I asked the model when chat history was enabled. This time, the model gave me study tips when I first asked it how to study more productively, but its responses to my next question was very general. I asked the model how to set realistic goals, as it recommended goal-setting as a way to improve my study habits, but its next response was focused on goal-setting in life in general, rather than studying. The model then asked me what my specific goal was, and I responded that I wanted to study more productuvely, effectively bringing the conversation back to where we had started. While the tips the model gave me were not completely unhelpful, not having access to our chat history prevented it from relating its current answers back to information from my previous questions (e.g., relating all its answers back to studying).

## Results - Colab

1. Run the code and create graphs of the results. Can you see any patterns to the mistakes each model makes or do they appear random? Do the all the models make mistakes on the same questions?

Results are for models run on GPUs with no quantization. Similar to the results obtained when running models locally, all models run on Colab (including the three additional medium-size models tested) performed the best on US foreign policy and the worst on professional accounting. Results for astronomy, business ethics, nutrition, philosophy and prehistory were similar, though not identical, for the three small models, similar except for business ethics on `Llama-3.1 8B` and `OLMo-2 7B`, and very similar for `Qwen-2.5 7B`. Overlap was particularly strong for astronomy, nutrition, philosophy, prehistory, public relations, security studies, sociology, and US foreign policy among the three largest models, suggesting that larger models are more consistent with one another than smaller models. This could be due to memorization or simply having learned certain concepts better. Overlap for professional accounting was low.

