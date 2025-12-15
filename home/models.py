from django.db import models
import os
import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver



def preprocessed_upload_path(instance, filename):
    base,ext = os.path.splitext(filename)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"dataset/preprocessed/{base}_{timestamp}{ext}"

# Create your models here.
class PreprocessedDataset(models.Model):
    file=models.FileField(upload_to=preprocessed_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Preprocessed dataset ({self.uploaded_at.strftime('%d/%m/%Y %H:%M:%S')})"

@receiver(post_delete, sender=PreprocessedDataset)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


class SentimentDataset(models.Model):
    file=models.FileField(upload_to="dataset/sentiment")
    generated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sentiment dataset ({self.generated_at.strftime('%d/%m/%Y %H:%M:%S')})"

@receiver(post_delete, sender=SentimentDataset)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)