from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from ..models import SentimentDataset
from .serializers import RankingSerializer

@api_view(['POST'])
def ranking_api(request):
    category = request.data.get("category")

    if category != "electronic":
        return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)

    dataset = SentimentDataset.objects.last()
    if not dataset:
        return Response({"message": "No dataset found"}, status=status.HTTP_404_NOT_FOUND)

    df = pd.read_csv(dataset.file.path)

    avg_score = df.groupby("eshop")['signed_score'].mean()
    review_count = df.groupby('eshop')['Summary'].count()

    k = 5
    weighted_score = (avg_score * (review_count / (review_count + k)))

    ranking_df = pd.DataFrame({
        'eshop': avg_score.index,
        'average_score': avg_score,
        'review_count': review_count,
        'weighted_score': weighted_score,
    })

    ranking_df = ranking_df.sort_values(by='weighted_score', ascending=False).reset_index(drop=True)

    serializer = RankingSerializer(ranking_df.to_dict(orient="records"), many=True)
    return Response(serializer.data)
