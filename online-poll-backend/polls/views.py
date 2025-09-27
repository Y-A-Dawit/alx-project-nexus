from django.shortcuts import render
from django.db import IntegrityError, transaction
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Poll, Choice, Vote
from .serializers import (
    PollListSerializer, PollDetailSerializer, PollCreateSerializer, ChoiceSerializer, VoteSerializer
)

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "create":
            return PollCreateSerializer
        if self.action == "retrieve":
            return PollDetailSerializer
        return PollListSerializer

# Vote endpoint: POST /api/polls/<poll_id>/vote/
class VoteAPIView(APIView):
    def post(self, request, poll_id):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        choice = serializer.validated_data["choice_obj"]
        voter_id = serializer.validated_data["voter_id"]

        # Check that the choice belongs to the poll_id
        if choice.poll_id != poll_id:
            return Response({"detail": "Choice does not belong to this poll."}, status=status.HTTP_400_BAD_REQUEST)

        # Create vote atomically, rely on unique_together to prevent duplicates
        try:
            with transaction.atomic():
                vote = Vote.objects.create(poll_id=poll_id, choice=choice, voter_id=voter_id)
        except IntegrityError:
            return Response({"detail": "You have already voted in this poll."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Vote recorded."}, status=status.HTTP_201_CREATED)

# Results endpoint: GET /api/polls/<poll_id>/results/
class ResultsAPIView(APIView):
    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response({"detail": "Poll not found."}, status=status.HTTP_404_NOT_FOUND)

        # Efficiently annotate vote counts per choice
        choices = Choice.objects.filter(poll=poll).annotate(vote_count=Count("votes")).values(
            "id", "choice_text", "vote_count"
        )

        data = {
            "poll_id": poll.id,
            "question": poll.question,
            "results": list(choices)
        }
        return Response(data)
