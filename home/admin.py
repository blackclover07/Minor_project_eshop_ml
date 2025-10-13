from django.contrib import admin
from home.models import PreprocessedDataset,SentimentDataset


# Register your models here.

@admin.register(PreprocessedDataset)
class PreprocessedDatasetAdmin(admin.ModelAdmin):
    list_display = ('file','uploaded_at')


@admin.register(SentimentDataset)
class SentimentDatasetAdmin(admin.ModelAdmin):
    list_display = ('file','generated_at')