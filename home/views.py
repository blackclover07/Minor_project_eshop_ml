
from django.shortcuts import render
import pandas as pd
from home.models import SentimentDataset


# Create your views here.
def index(request):
    if request.method == "POST":
        category = request.POST.get("category")
        if category == "electronic":
            dataset=SentimentDataset.objects.last()
            if not dataset:
                return render(request,'index.html',{'ranking':None,'message':'No dataset found'})
            # load csv
            df=pd.read_csv(dataset.file.path)
            # computing avg score
            avg_score=df.groupby("eshop")['signed_score'].mean()

            # weighted score
            review_count=df.groupby('eshop')['Summary'].count()
            k=5   #smoothing factor
            weighted_score=(avg_score*(review_count/review_count+k))

            # prepare the dataset
            ranking_df=pd.DataFrame({
                'eshop':avg_score.index,
                'average_score':avg_score,
                'review_count':review_count,
                'weighted_score':weighted_score,
            })

            ranking_df= ranking_df.sort_values(by='weighted_score',ascending=False).reset_index(drop=True)
            ranking=ranking_df.to_dict(orient='records')
            return render(request,'index.html',{'ranking':ranking})
    return render(request,"index.html")
