from django import forms

from enterprises.models import ContactFormSubmission


class ContactForm(forms.ModelForm):
    """A simple comment form."""

    class Meta:
        model = ContactFormSubmission
        fields = ["name", "reply_email", "submission"]
        labels = {
            "name": "Full Name",
            "reply_email": "Email",
            "submission": "Comment",
        }
        widgets = {
            "submission": forms.Textarea(attrs={"rows": 5, "maxlength": 2000}),
        }
