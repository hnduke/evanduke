import logging

from django import forms
from django.core.exceptions import BadRequest, ValidationError
from google.auth.exceptions import DefaultCredentialsError, MutualTLSChannelError

from enterprises.models import ContactFormSubmission
from enterprises.recaptcha import is_human

logger = logging.getLogger(__file__)

SUBMISSION_CHAR_LIMIT = 1000


class ContactForm(forms.ModelForm):
    """A simple comment form."""

    action = "contact"

    class Meta:
        model = ContactFormSubmission
        fields = ["name", "reply_email", "submission"]
        labels = {
            "name": "Full Name",
            "reply_email": "Email",
            "submission": "Comment",
        }
        widgets = {
            "submission": forms.Textarea(
                attrs={"rows": 5, "maxlength": SUBMISSION_CHAR_LIMIT}
            ),
        }

    def clean_submission(self):
        submission = self.cleaned_data.get("submission")
        if submission and len(submission) <= SUBMISSION_CHAR_LIMIT:
            return submission
        raise ValidationError(
            f"The maximum number of characters allowed is {SUBMISSION_CHAR_LIMIT}"
        )

    def clean(self):
        """Check the reCAPTCHA in addition to everything else.

        Raises BadRequest if reCAPTCHA concludes that something is fishy.
        """

        super().clean()
        captcha = self.data.get("g-recaptcha-response")
        try:
            valid = is_human(captcha, self.action)
        except (DefaultCredentialsError, MutualTLSChannelError) as e:
            logger.exception(e)
            self.add_error(
                "submission",
                "We are sorry, but we're experiencing some difficulties with our provider just now. Please "
                "try again in a few minutes.",
            )
            return

        if not valid:
            raise BadRequest
