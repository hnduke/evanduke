from django.db import models


class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    reply_email = models.CharField(max_length=256)
    submission = models.TextField()

