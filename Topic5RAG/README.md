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

NOTE: for this experiment, I use Gemini as the frontier model.

1. Where does the frontier model's general knowledge succeed?

   Gemini seems to use a web search tool for most of the congressional proceedings questions, so my focus in this answer will be on the Model T queries.
   Because it was difficult to pinpoint exact ground truth answers in the manual, I do not have exact ground truth answers to compare the model responses
   to, but the model responses contained a good amount of information organized in a way such that it was easy to follow and often provided additional
   information, explanations, and reccomenndations that, if true, could benefit someone might want to know why something works the way it does or what
   additional options they have if they are using the model to help them repair a Model T.

3. When did the frontier model appear to be using live web search to help answer your questions?

   Some of the more obvious instances of models using live web search were when the model gave information on the congressional proceedings from January 2026. Since these
   proceedings happened fairly recently, the fact that the model was able to summarize them suggests that it used some kind of web search. The only exception might be the
   model's response to the question "What mistake Elise Stefanovic make in Congress on January 23, 2026?", as the model was not able to find the correct answer. It did
   provide other information about Elize Stefanovic, which could have been the result of a web search that simply failed to identify the answer from the proceedings document.
   As for the questions about the Model T, it is less clear whether the model is calling a web search tool or is simply generating information about the Model T that it
   learned from its training text, as there are no clear citations or notes made to indicate that a web search was performed.
   
4. Where does your RAG system provide more accurate, specific answers?

   The RAG answers were not necessarily more accurate than the Gemini answers, but they were generally more concise (my point of reference for this is mostly from the
   answers about the congressional proceedings, as the accuracy of these responses was far easier to determine). Overall, Gemini's answers contained more specific
   and detailed information while the RAG answers were shorter and were formatted more as higher-level summaries.

6. What does this tell you about when RAG adds value vs. when a powerful model suffices?

   RAG models seem to be most useful when the user wants short, concise steps/summaries as opposed to longer explanations. Having additional details and
   explanations is useful when one wants to dive in deeper into a particular subject, but having access to a shorter summary drawn from a database of
   relevant information might be more helpful in getting the general idea more quickly.


## Experiment 4

For this question, I prompted the model to retrieve information from the EU AI Act using the following three queries:

- In what ways can AI systems benefit society?
- What are the risks of AI systems built to detect human emotions?
- What practices are developers of open-source AI that is not general-purpose AI encouraged to follow?

Each query is based off of a paragraph I found in the EU AI Act so the model should have at least those references for its answers.

1. At what point does adding more context stop helping?

This depends on the query. For query number 1, as k increased, the model responses became more general, circular, and less grounded in providing a precise answer based on the question. This suggests that having too much context can result in the model trying to incorporate everything it finds without being able to prioritize a few key points that most concretely answer the question. For query number 2, more information was included in the responses as k increased, but this additional information was still concrete and relevant (though some of it seemed to be taken from other parts of the AI Act than I had originally used to construct the query). For query number 3, the opposite effect was observed: it was only with higher values of k that the model was able to cite the specific paragraph I had based my query off of in its answer. Answers with k < 10 stated that they could not find the exact information requested based off of the query, suggesting that the paragraph I was referencing only appeared in the context with larger k. These varying results reveal a potential tradeoff in wanting a lower k for more general questions whose answers could be found in multiple parts of the reference document versus wanting a higher k for more specific questions that reference a particular paragraph. 

2. When does too much context hurt (irrelevant information, confusion)?

Negative consequences for higher values of k were most pronounced in the responses to query number one, where the model's answers became very general, circular, and less focused on precicely answering the question. This query might have been sensitive to too much context because it is very general, where its answer can be easily constructed from various chunks in the text. This would result in too much information needing to be aggregated and condensed, leading the model to lose its focus on the specifics of the question being asked.

3. How does k interact with chunk size?

The larger the chunk size, the more information is likely to be stored in any given chunk. More information contained in a single chunk implies that a smaller k might be used without much information loss, as this smaller set of chunks might contain as much, if not more, information than a larger number of chunks with less information contained in each. So the larger the chunk size, the smaller k can be without risking losing information.

## Experiment 5

For this experiment, I used the three queries provided in the experiment description:

- "What is the capital of France?"
- "What's the horsepower of a 1925 Model T?" (if not in your manual)
- "Why does the manual recommend synthetic oil?" (when it doesn't)

1. Does the model admit it doesn't know?

For the first two queries, the model states that the answer cannot be found in the context so it cannot produce a response. For the last query, the model attempts to provide an explanation for why synthetic oils are recommended despite a lack of context but eventually admits that it would need definitive information from the context to be more certain in its answer and explanations. 

3. Does it hallucinate plausible-sounding but wrong answers?

The closest the model gets to a hallucination is in its answer to the third query about synthetic oils. The model's response attempts to operate under the premise that the manual did recommend synthetic oils, even citing specific sections of the manual in its answer, though these quotes only generally refer to oil use in the Model T. The model attempts to draw a connection between these quotes and the supposed premise that synthetic oil is recommended, but the connection is very forced and it is obvious that the model is trying its best to find evidence for why the prompt's premise could be true.

4. Does retrieved context help or hurt? (Does irrelevant context encourage hallucination?)
   TODO

5. Experiment: Modify your prompt template to add "If the context doesn't contain the answer, say 'I cannot answer this from the available documents.'" Does this help?
   TODO

























