import pytest
from django.urls import reverse

from enterprises.models import ContactFormSubmission, ServiceType


def test_faqs_view_for_fractional_management(client, faqs):
    url = reverse("faqs", kwargs={"service_type": ServiceType.FRACTIONAL_MANAGEMENT.name})
    response = client.get(url)
    assert response.status_code == 200
    assert all(faq.service_type == ServiceType.FRACTIONAL_MANAGEMENT.value for faq in response.context["faqs"])


def test_faqs_view_for_consultations(client, faqs):
    url = reverse("faqs", kwargs={"service_type": ServiceType.CONSULTATIONS.name})
    response = client.get(url)
    assert response.status_code == 200
    assert all(faq.service_type == ServiceType.CONSULTATIONS.value for faq in response.context["faqs"])


def test_faqs_view_with_invalid_service_type(client):
    url = reverse("faqs", kwargs={"service_type": "INVALID_TYPE"})
    response = client.get(url)
    assert response.status_code == 404


# Test for ContactView
def test_contact_view_get(client):
    response = client.get(reverse("contact"))
    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_contact_view_post_valid(client, mocker):
    mocker.patch("enterprises.forms.is_human").return_value = True
    response = client.post(
        reverse("contact"),
        {
            "name": "Test",
            "reply_email": "test@example.com",
            "submission": "Hello",
            "g-recaptcha-response": "PASSED",
        },
    )
    assert response.status_code == 302
    assert response.url == reverse("thank-you")

    submission = ContactFormSubmission.objects.last()
    assert submission
    assert submission.name == "Test"
    assert submission.reply_email == "test@example.com"
    assert submission.submission == "Hello"


# Test for thank_you view
def test_thank_you_view_no_session(client):
    response = client.get(reverse("thank-you"))
    assert response.status_code == 302
    assert response.url == reverse("contact")


@pytest.mark.django_db
def test_thank_you_view_with_session(client):
    submission = ContactFormSubmission.objects.create(name="Test", reply_email="test@example.com", submission="Hello")
    session = client.session
    session["submission-uuid"] = str(submission.id)
    session.save()

    response = client.get(reverse("thank-you"))
    assert response.status_code == 200
    assert response.context["submission"].id == submission.id


def test_index_page_loads_correctly(client):
    response = client.get(reverse("index"))
    assert response.status_code == 200


def test_about_page_loads_correctly(client):
    response = client.get(reverse("about"))
    assert response.status_code == 200
