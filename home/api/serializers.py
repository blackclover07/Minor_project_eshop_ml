from rest_framework import serializers

class RankingSerializer(serializers.Serializer):
    eshop = serializers.CharField()
    average_score = serializers.FloatField()
    review_count = serializers.IntegerField()
    weighted_score = serializers.FloatField()

