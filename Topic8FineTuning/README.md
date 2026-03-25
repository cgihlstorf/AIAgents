# Table of Contents

- `tinker-cookbook`: link to the Tinker Cookbook repository
- `base_model_results.txt`: results from running the base model on the test examples
- `finetune.y`: code used to run the base model, finetune the model, and eveluate it on the test set and the challenge set
- `finetuned_model_challenge_inputs_responses.txt`: results from running the fintuned model on the challenge examples
- `finetuned_model_results.txt`: results from running the finetuned model on the test examples
- `gemini_sql_challenge_set_answers.txt`: file comparing results from running the finetuned model on the test set to ground truth answers obtained from prompting Gemini
- `sql_create_context_v4.json`: examples used to train and evaluate the models
- `sql_matches.py`: file containing helper functuons to evaluate the SQL outputs from the model


# Results/Analysis

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

This analysis is focused on the finetuned model's performance on the challenge set. As mentioned above, the model only got 1 out of the 5 questions correct. Below, I lay out the ground truth answers from Gemini and compare them to the finetuned model's responses for each question. These results can also be found in `gemini_sql_challenge_set_answers.txt`. Results for just the finetuned model on the challenge set can be found in `finetuned_model_challenge_inputs_responses.txt`. 

#### Question: What are the names of employees in the engineering department?
- Ground Truth Answer (Gemini): `SELECT name FROM employees WHERE department = 'engineering';`
- Finetuned Model Answer: `SELECT MAX(id) FROM employees WHERE salary > 100000 AND department = 'engineering'`

**Analysis**: The model makes two mistakes here. First, it uses `SELECT MAX(id)` instead of `SELECT name`. It also includes the condition that the employee's salary be greater than $100,000, which was not a specification of the orginal question.

#### Question: How many products cost more than 50 dollars?
- Ground Truth Answer (Gemini): `SELECT COUNT(*) FROM products WHERE price > 50;`
- Finetuned Model Answer: `SELECT SUM(id) FROM products WHERE price > 50 AND category = 'electronics'`

**Analysis**: The model makes similar errors here to those from the first question. Instead of using `SELECT COUNT(*)`, the model uses `SELECT SUM(id)` instead (after asking Gemini about this, I learned that these are two different functions). Additionally, the model specifies that the produces should be limited to electronics, which was not specified in this original question.

#### Question: What is the highest score in the science class?
- Ground Truth Answer (Gemini): `SELECT MAX(score) FROM students WHERE class = 'science';`
- Finetuned Model Answer: `SELECT MAX(score) FROM students WHERE class = 'Science'`

**Analysis**: The model answers this question correctly (assuming the capitalization of 'science' makes no difference here).

#### Question: List the top 3 customers by total order amount.
- Ground Truth Answer (Gemini): `SELECT customer, SUM(amount) AS total_spent`
`FROM orders`
`GROUP BY customer`
`ORDER BY total_spent DESC`
`LIMIT 3;`
- Finetuned Model Answer: `SELECT MAX(id), customer FROM orders GROUP BY customer ORDER BY SUM(amount) DESC LIMIT 3`

**Analysis**: The model's answer does not align with the ground truth answer. Although a few keyword phrases in the model's answer match those in the ground truth, the model's syntax is off and does not call all of the same things in the same order that the ground truth query does. The model's incorrect answer makes sense here, since this is a more difficult query.

#### Question: How many students are enrolled in each department?
- Ground Truth Answer (Gemini): `SELECT c.department, COUNT(e.student_id) AS student_count`
`FROM courses c`
`JOIN enrollments e ON c.id = e.course_id`
`GROUP BY c.department;`
- Finetuned Model Answer: `SELECT SUM(T1.student_id), T1.name, T2.department FROM enrollments AS T1 JOIN courses AS T2 ON T1.course_id = T2.id GROUP BY T2.department`

**Analysis**: I asked Gemini whether these two queries were the same, as they seemed to contain similarly-named references but I wasn't sure whether they meant the same thing or not. According to Gemini, these queries are not the same, and the finetuned model's answer acrually contains a syntax error that makes it invalid SQL. Similarly to some of the model's previous answers, it uses column ids instead of the actual information it needs from the columns, which might be a mistake it learned during training — that is, to associate column ids with the actual information in the columns that it needs.