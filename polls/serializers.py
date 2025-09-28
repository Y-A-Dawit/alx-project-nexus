from rest_framework import serializers
from .models import Poll, Choice, Vote

class ChoiceSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Choice
        fields = ("id", "choice_text", "vote_count")


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ("id", "question", "created_at", "expiry_date")


class PollDetailSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ("id", "question", "created_at", "expiry_date", "choices")


class PollCreateSerializer(serializers.ModelSerializer):
    # Accept a list of strings for choices
    choices = serializers.ListField(
        child=serializers.CharField(max_length=255),
        write_only=True,
        min_length=1
    )

    class Meta:
        model = Poll
        fields = ("id", "question", "expiry_date", "choices")

    def create(self, validated_data):
        choices_data = validated_data.pop("choices", [])
        poll = Poll.objects.create(**validated_data)
        choice_objs = [Choice(poll=poll, choice_text=text) for text in choices_data]
        Choice.objects.bulk_create(choice_objs)
        return poll


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()
    voter_id = serializers.CharField(max_length=255)

    def validate(self, data):
        choice_id = data.get("choice_id")
        try:
            choice = Choice.objects.select_related("poll").get(id=choice_id)
        except Choice.DoesNotExist:
            raise serializers.ValidationError({"choice_id": "Choice not found."})
        data["choice_obj"] = choice
        return data
