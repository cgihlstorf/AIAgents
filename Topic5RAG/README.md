## Experiment 1

### Does the model hallucinate specific values without RAG?

The model did hallucinate some specific values. For example, when asked what type of oil should be used in a Model T, the model responded 
with "motor oil" as the answer, but a quick command+f search through the manual did not find any instances of that phrase. In another instance 
when asked what Mr. Flood said about Mayor David Black, the model stated that Mayor Black was the mayor of New York, when in reality 
he was the mayor of Papillion, Nebraska. The model also completely hallucinated the answer to the question 
"What mistake Elise Stefanovic make in Congress on January 23, 2026?", claiming that her mistake was saying that the United States was not a
democracy when in reality the mistake was that she accidentally cast a "no" vote instead of a "yes" vote.

### Does RAG ground the answers in the actual manual?

For the Model T corpus questions, the RAG answers seemed solidly grounded in the manual for all questions except question 2. 
For question 2 ("What is the correct spark plug gap for a Model T Ford?") I could not find the value produced by the model in the manual,
suggesting that the value was hallucinated. For question 4 ("What oil should I use in a Model T engine?"), the model expressed in its answer that it could not find the information in the manual it was given, suggesting that it did attempt to reference the manual but failed to find the answer. This aligns with my own experience of doing a keyword search for "motor oil" but getting no results.



### Are there questions where the model's general knowledge is actually correct?

It is harder for me to determine the exact level of correctness of the model with the default prompt on the Model T questions as I am not
an expert in that area, so this answer focuses mostly on the congressional proceedings text. For most of the questions, the model with the
default prompt seems to hallucinate most of its answers, even if small pieces of information it provides are not completely incorrect. For example, when asked about what Mr. Flood said about Mayor David Black the model correctly stated that the mayor was not going to run for re-election but hallucinated that the mayor was from New York as opposed to Papillion, Nebraska. The model gets one key detail correct in this case, but hallucinates other details. 


## Experiment 2

- NOTE 1: for this experiment I used ChatOllama with `qwen3-next:80b-cloud` instead of `gpt4-mini`.
- NOTE 2: the code to run the model for this task can be found in `larger_model_no_RAG.py`


### Does Qwen3-next80b do a better job than Qwen 2.5 1.5B in avoiding hallucinations?

`Qwen3-next80b` seems to hallucinate slightly less than `Qwen25-1.5b`, though I was unable to verify a few of its answers because the questions did not specify 
information needed in order to most precisely answer the question. This informations includes specifying that questions about cars refer to Model T cars (question 3 about the 
Model T does not specofy this) and specifying the specific date of congressional proceedings being referenced (question 4 about the congressional proceedings does not
include a date or mention specific proceedings). Thus, there is no ground truth readily available to compare with these answers to determine if they are hallucinations
or not. There were a couple of times when the model said that it could not answer a congressional proceedings questiion because it did not have the information from
that far into the future, which helped prevent possible hallucinating false information in those cases.


### Which questions does Qwen3-next80B answer correctly? Compare the cut-off date of Qwen3-next80b pre-training and the age of the Model T Ford and Congressional Record corpora.

It is difficult to determine the extent to which the model answers questions correctly for a few reasons: first, sometimes the model refuses to answer the question because its 
knowledge cutoff is too far in the past, but it still provides information it claims it knows about the general topic at hand, which is not able to be verified with the ground
truth documents provided. Second, I often couldn't find a ground truth answer for questions about the Model T after a few keyword searches in the manual, so I had nothing to compare the models' answers to. But given that I couldn't find couple of the model's answers via keyword search in the manual, it is possible that the models hallucinated their answers or are using some other data source (perhaps another manual) to inform their responses. Third, as mentioned in the previous answer, there are a couple of questions that do not 
provide enough specifics (e.g., that the car in question is a Model T or that the question refers to specific congressional proceedings on a specific date). Given that the model's knowledge cutoff date seems to be before January 2026, it makes sense that it would either refuse to answer the questions that asked about specific dates after it was trained. The model never refused to answer questions about the Model T, however, suggesting that it had some information in its training corpus to draw from (which makes sense, as the Model T was introduced over 100 years ago). Even so, I could not fully verify its responses in the manual provided, suggesting that there might be another manual that I should e checking instead
or that the model is hallucinating some or all of its responses.


## Experiment 3

1. Where does the frontier model's general knowledge succeed?

   TODO

3. When did the frontier model appear to be using live web search to help answer your questions?

   TODO

5. Where does your RAG system provide more accurate, specific answers?

   TODO

6. What does this tell you about when RAG adds value vs. when a powerful model suffices?

   TODO















