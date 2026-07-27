from django.urls import path

from .views import RecommendationView

urlpatterns = [

    path(
        "<int:category_id>/",
        RecommendationView.as_view(),
        name="recommendations",
    ),

]