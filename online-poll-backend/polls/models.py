from django.db import models

# Create your models here.
from django.db import models

class Poll(models.Model):
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Poll({self.id}): {self.question[:50]}"


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return f"Choice({self.id}) for Poll({self.poll_id}): {self.choice_text[:30]}"


class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name="votes", on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name="votes", on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=255)  # e.g., user id, session id, or ip address
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("poll", "voter_id")  # prevents duplicate votes by same voter for a poll

    def __str__(self):
        return f"Vote({self.id}) poll={self.poll_id} choice={self.choice_id} voter={self.voter_id}"
