import pandas as pd
from tqdm import tqdm
import os
from home.models import SentimentDataset
from django.core.files import File
# Global variable to cache the model
_cardiff_pipeline = None

def get_cardiff_pipeline():
    """
    Load the HuggingFace pipeline only once per session.
    """
    global _cardiff_pipeline
    if _cardiff_pipeline is None:
        from transformers import pipeline
        import torch

        device = -1  # CPU for dev, change to 0 for GPU
        cardiff_model = "cardiffnlp/twitter-roberta-base-sentiment-latest"

        print("🔄 Loading Cardiff sentiment pipeline...")
        _cardiff_pipeline = pipeline(
            "sentiment-analysis",
            model=cardiff_model,
            tokenizer=cardiff_model,
            device=device
        )
        print("✅ Pipeline loaded!")
    return _cardiff_pipeline

def cardiff_sentiment(text):
    """
    Compute sentiment for a single text using the cached pipeline.
    """
    pipeline = get_cardiff_pipeline()  # load once
    res = pipeline(text, truncation=True, max_length=512)[0]
    label = res["label"].lower()
    score = res["score"]
    signed_score = score if label == "positive" else -score if label == "negative" else 0.0
    return {"label": label, "score": score, "signed_score": signed_score}

from django.core.files.base import ContentFile

def sentiment_analysis(input_csv_path):
    df = pd.read_csv(input_csv_path)
    results = []

    for review in tqdm(df["Summary"].dropna(), desc="Processing reviews", colour="blue"):
        if not isinstance(review, str) or not review.strip():
            continue
        results.append(cardiff_sentiment(review))

    results_df = pd.DataFrame(results)
    final_df = pd.concat([df.reset_index(drop=True), results_df], axis=1)

    # Convert DataFrame to CSV in memory
    csv_content = final_df.to_csv(index=False)
    django_file = ContentFile(csv_content.encode("utf-8"))

    # Save to Django model
    base_name = os.path.splitext(os.path.basename(input_csv_path))[0]
    sentiment_instance = SentimentDataset()
    sentiment_instance.file.save(f"{base_name}_sentiment.csv", django_file, save=True)

    print(f"✅ SentimentDataset entry created: {sentiment_instance.file.url}")
    return base_name,sentiment_instance
