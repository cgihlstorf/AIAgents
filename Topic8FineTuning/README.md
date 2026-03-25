## Base Model Results

The base model achieved an accuracy of 50% on the test examples. Results for the base model can be found in `base_model_results.txt`.

## Finetuned Model Results

The finetuned model achieved an accuracy of 90% on the test examples. Results for the finetuned model can be found in `finetuned_model_results.txt`.

## Challenge Schema Results

I prompted Gemini to get ground truth answers for each query. I compared Gemini's answers to the model's answers and found that the model only got 1 out of 5 questions correct. For the questions it answered incorrectly, it most oftne got some, but not all, of the syntax correct, demonstrating it had an idea of what to do but was not able to produce a fully correct answer. 

## Discussion Questions

### Before vs. after: What specific improvements did you observe? Did the model learn SQL syntax, schema grounding, or both? What was the change in accuracy on the 200 held-out test questions? How well did it do on the additional manual test questions (Step 7)?

The finetuned model outperformed the base model by 40 percentage points, suggesting a large improvement in knowledge of SQL. As mentioned above, the finetuned model only got one of the 5 challenge questions correct, but its answers for the remaining challenge questions still indivate some level of understanding, just with some errors that prevent the answer from being entirely correct. For example, for the first question, *What are the names of employees in the engineering department?* the ground truth answer was `SELECT name FROM employees WHERE department = 'engineering';` while the model's answer was `SELECT MAX(id) FROM employees WHERE salary > 100000 AND department = 'engineering'`. While the model seems to have an idea of what to search for, it uses the incorrect search term `SELECT MAX(id)` and adds an unnecessary specification of selecting employees with salaries greather than $100,000. Some of its other incorrect answers are similar to this in that they often get some of the syntax correct but they make a wrong selection and/or include additional specifications that weren't asked for in the question.

### RAG comparison: Imagine you had a RAG system with 1,000 (question, SQL) pairs in a vector database. For which of the test questions above would RAG work well? For which would it struggle? Why?

In general, a RAG system would work better when the questions in the database were either identical or semantically similar to the question posed to the model. The more the input question falls within the distribution of questions in the RAG database, the more likely the model is to successfully retrieve the correct SQL via RAG. So, the RAG model would work better with questions that ressembled the questions in the vector database, while it would struggle with questions that were more out of distribution. 

### Error analysis: When the fine-tuned model gets a query wrong, how does it fail? Wrong column names? Wrong SQL syntax? Wrong logic? Each failure mode tells you something different about what the model learned.

This analysis is focused on the finetuned model's performance on the challenge set. 