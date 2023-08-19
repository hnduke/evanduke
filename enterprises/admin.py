from django.contrib import admin

from enterprises.models import FrequentlyAskedQuestion


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "answer", "ordering", "service_type"]
    ordering = ["ordering"]
