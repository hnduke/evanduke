from enum import Enum

from django.db import models


class ServiceType(Enum):
    FRACTIONAL_MANAGEMENT = "Fractional Management"
    CONSULTATIONS = "Consultations"


class FrequentlyAskedQuestion(models.Model):
    question = models.TextField()
    answer = models.TextField()
    ordering = models.IntegerField()
    service_type = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in ServiceType],
        default=ServiceType.FRACTIONAL_MANAGEMENT.value,
    )

    class Meta:
        ordering = ["ordering"]

    def __str__(self):
        return self.question[:25] + ("..." if len(self.question) > 25 else "")


class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    reply_email = models.CharField(max_length=256)
    submission = models.TextField()
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Note from {self.name or self.reply_email}"
