from rest_framework.generics import ListAPIView

from .serializers import RecommendationSerializer
from .services import RecommendationService


class RecommendationView(ListAPIView):

    serializer_class = RecommendationSerializer

    def get_queryset(self):

        category_id = self.kwargs["category_id"]

        return RecommendationService.recommended_products(
            category_id
        )