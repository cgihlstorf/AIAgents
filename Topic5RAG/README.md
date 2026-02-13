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

The closest the mode

