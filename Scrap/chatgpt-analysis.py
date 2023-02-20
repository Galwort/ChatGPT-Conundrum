from pandas import DataFrame, read_csv
from transformers import pipeline, AutoTokenizer

# downloading the model and tokenizer
detector = pipeline("text-classification", model="roberta-base-openai-detector")
tokenizer = AutoTokenizer.from_pretrained("roberta-base-openai-detector")

chatgpt_df = read_csv("chatgpt-abstracts.csv")
abs_df = DataFrame(
    columns=[
        "journal",
        "abstract",
        "characters",
        "tokens",
        "score"
    ]
)

for index, row in chatgpt_df.iterrows():
    result = detector(row["abstract"])
    tokens = tokenizer.tokenize(row["abstract"])
    abs_df = abs_df.append({
        "journal": row["journal"],
        "abstract": row["abstract"],
        "characters": len(row["abstract"]),
        "tokens": len(tokens),
        "score": result[0]["score"] if result[0]["label"] == "Fake" else 1 - result[0]["score"]
    }, ignore_index=True)

abs_df.to_csv("chatgpt-analysis.csv", index=False)