from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PreprocessedDataset
from .utils.Sentiment_analyzer import sentiment_analysis
import threading
import time

def run_ml_in_background(input_csv_path):
    # Optional: wait 2 seconds before starting
    time.sleep(2)
    sentiment_analysis(input_csv_path)

@receiver(post_save, sender=PreprocessedDataset)
def trigger_sentiment_analysis(sender, instance, created, **kwargs):
    if created:
        input_csv_path = instance.file.path
        print(f"📝 New dataset uploaded: {input_csv_path}")
        # Run ML in a background thread
        threading.Thread(target=run_ml_in_background, args=(input_csv_path,)).start()
        print("🚀 Sentiment analysis started in background!")
