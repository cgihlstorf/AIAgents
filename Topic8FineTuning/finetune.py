import tinker
from tinker import types
from datasets import load_dataset
import json, random, sqlite3
from sql_matches import sql_matches


def sample_from_model(sampling_client, tokenizer, context: str, question: str) -> str:

    """Generate SQL from the model given schema and question."""
    prompt = f"""Table schema:
    {context}
    Question: {question}
    SQL: """

    prompt_tokens = tokenizer.encode(prompt, add_special_tokens=True)
    model_input = types.ModelInput.from_ints(tokens=prompt_tokens)
    params = types.SamplingParams(max_tokens=150, temperature=0.0, stop=["\n\n", "Question:"])
    result = sampling_client.sample(prompt=model_input, sampling_params=params, num_samples=1).result()
    
    if result.sequences:
        return tokenizer.decode(result.sequences[0].tokens).strip()
    return ""


def eval_one(sampling_client, tokenizer, ex: dict) -> bool:
    """Evaluate one example: generate SQL, then check if it matches expected."""
    sql = sample_from_model(sampling_client, tokenizer, ex["context"], ex["question"])
    return sql_matches(sql, ex["answer"], schema=ex["context"])

def evaluate_test_set(sampling_client, tokenizer, test_data: list) -> float:
    """Compute accuracy = fraction of test examples where generated SQL matches expected."""
    correct = sum(1 for ex in test_data if eval_one(sampling_client, tokenizer, ex))
    return correct / len(test_data)


def run_base_model(test_data):

    service_client = tinker.ServiceClient()
    base_model = "meta-llama/Llama-3.2-1B"
    training_client = service_client.create_lora_training_client(base_model=base_model)
    tokenizer = training_client.get_tokenizer()

    print("\n--- Evaluating Base Model on 200 Test Questions ---")
    base_sampling_client = training_client.save_weights_and_get_sampling_client(
        name="base-model"
    )
    base_accuracy = evaluate_test_set(
        base_sampling_client, tokenizer, test_data, "base"
    )
    print(f"Base model accuracy: {base_accuracy:.2%} ({int(base_accuracy * 200)}/200)")



if __name__ == "__main__":

    #Load data
    with open("sql_create_context_v4.json") as f:
        data = json.load(f)

    NUM_TEST_EXAMPLES = 200  # Held-out for evaluation; all remaining data used for training
    random.shuffle(data)
    test_data = data[:NUM_TEST_EXAMPLES]
    train_data = data[NUM_TEST_EXAMPLES:]

    run_base_model(test_data)









# service_client = tinker.ServiceClient()
# training_client = service_client.create_lora_training_client(
#     base_model="meta-llama/Llama-3.2-1B",
#     rank=32,
# )
# tokenizer = training_client.get_tokenizer()

# examples = [
#     {"input": "banana split",      "output": "anana-bay plit-say"},
#     {"input": "quantum physics",   "output": "uantum-qay ysics-phay"},
#     {"input": "donut shop",        "output": "onut-day op-shay"},
#     {"input": "pickle jar",        "output": "ickle-pay ar-jay"},
#     {"input": "space exploration", "output": "ace-spay exploration-way"},
#     {"input": "rubber duck",       "output": "ubber-ray uck-day"},
#     {"input": "coding wizard",     "output": "oding-cay izard-way"},
# ]


# def process_example(example, tokenizer):
#     prompt = f"English: {example['input']}\nPig Latin:"

#     # Tokenize prompt — the model sees this but is NOT trained on it
#     prompt_tokens = tokenizer.encode(prompt, add_special_tokens=True)
#     prompt_weights = [0] * len(prompt_tokens)

#     # Tokenize completion — the model IS trained to produce this
#     completion_tokens = tokenizer.encode(
#         f" {example['output']}\n\n", add_special_tokens=False
#     )
#     completion_weights = [1] * len(completion_tokens)

#     # Concatenate and shift for next-token prediction
#     tokens = prompt_tokens + completion_tokens
#     weights = prompt_weights + completion_weights

#     input_tokens = tokens[:-1]
#     target_tokens = tokens[1:]
#     weights = weights[1:]

#     return types.Datum(
#         model_input=types.ModelInput.from_ints(tokens=input_tokens),
#         loss_fn_inputs=dict(weights=weights, target_tokens=target_tokens),
#     )

# processed = [process_example(ex, tokenizer) for ex in examples]


# import numpy as np

# for step in range(6):
#     # Forward + backward: compute gradients on Tinker's GPUs
#     fwdbwd_future = training_client.forward_backward(
#         processed, "cross_entropy"
#     )

#     # Optimizer step: update the LoRA adapter weights
#     optim_future = training_client.optim_step(
#         types.AdamParams(learning_rate=1e-4)
#     )

#     # Wait for results and compute loss
#     fwdbwd_result = fwdbwd_future.result()
#     optim_result = optim_future.result()

#     logprobs = np.concatenate(
#         [out['logprobs'].tolist()
#          for out in fwdbwd_result.loss_fn_outputs]
#     )
#     weights = np.concatenate(
#         [ex.loss_fn_inputs['weights'].tolist()
#          for ex in processed]
#     )
#     loss = -np.dot(logprobs, weights) / weights.sum()
#     print(f"Step {step}: loss = {loss:.4f}")


# def get_responses():

#     sampler = training_client.save_weights_and_get_sampling_client(
#         name="pig-latin-model"
#     )
#     prompt = types.ModelInput.from_ints(
#         tokenizer.encode("English: coffee break\nPig Latin:")
#     )
#     params = types.SamplingParams(
#         max_tokens=20, temperature=0.0, stop=["\n"]
#     )
#     result = sampler.sample(
#         prompt=prompt, sampling_params=params, num_samples=8
#     ).result()

#     print("Responses:")
#     for i, seq in enumerate(result.sequences):
#         print(f"  {i}: {tokenizer.decode(seq.tokens)}")