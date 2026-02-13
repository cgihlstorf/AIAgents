from langchain_ollama import ChatOllama


def main():

    model = ChatOllama( #no tools
        model="qwen3-next:80b-cloud",
        temperature=0.7,
        max_tokens=256,
    )

    QUERIES_MODEL_T = [
        "How do I adjust the carburetor on a Model T?",
        "What is the correct spark plug gap for a Model T Ford?",
        "How do I fix a slipping transmission band?",
        "What oil should I use in a Model T engine?",
    ]

    QUERIES_CR = [
        "What did Mr. Flood have to say about Mayor David Black in Congress on January 13, 2026?",
        "What mistake did Elise Stefanik make in Congress on January 23, 2026?",
        "What is the purpose of the Main Street Parity Act?",
        "Who in Congress has spoken for and against funding of pregnancy centers?",
    ]

    for i in range(len(QUERIES_MODEL_T)):

        question_id = f"ford_{i}"
        question = QUERIES_MODEL_T[i]

        response = model.invoke(question).content

        with open(f"direct_answer_qwen3_next80b_{question_id}.txt", 'w') as f:
            f.write("Question: " + question + "\n\n" + response)

    for i in range(len(QUERIES_CR)):

        question_id = f"congress_{i}"
        question = QUERIES_CR[i]

        response = model.invoke(question).content

        with open(f"direct_answer_qwen3_next80b_{question_id}.txt", 'w') as f:
            f.write("Question: " + question + "\n\n" + response)

    

if __name__ == "__main__":
    main()