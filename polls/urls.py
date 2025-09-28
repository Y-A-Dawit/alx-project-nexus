from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, VoteAPIView, ResultsAPIView, home

router = DefaultRouter()
router.register(r"polls", PollViewSet, basename="poll")

urlpatterns = [
    path("", include(router.urls)),
    path("polls/<int:poll_id>/vote/", VoteAPIView.as_view(), name="poll-vote"),
    path("polls/<int:poll_id>/results/", ResultsAPIView.as_view(), name="poll-results"),
]
