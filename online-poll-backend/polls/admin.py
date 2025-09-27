# Register your models here.
from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class PollAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "created_at", "expiry_date")
    inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "poll", "choice_text")

class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "poll", "choice", "voter_id", "voted_at")
    search_fields = ("voter_id",)

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote, VoteAdmin)
