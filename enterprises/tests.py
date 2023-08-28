import pytest
from django.urls import reverse

from enterprises.models import FrequentlyAskedQuestion, ServiceType
from enterprises.recaptcha import is_human


@pytest.fixture
def faqs(db):
    faqs = []
    for service_type in ServiceType:
        for i in range(3):  # Creating 3 FAQs for each service type
            faq = FrequentlyAskedQuestion.objects.create(
                question=f"Question {i} for {service_type.name}",
                answer=f"Answer {i} for {service_type.name}",
                ordering=i,
                service_type=service_type.value,
            )
            faqs.append(faq)
    return faqs


def test_faqs_view_for_fractional_management(client, faqs):
    url = reverse(
        "faqs", kwargs={"service_type": ServiceType.FRACTIONAL_MANAGEMENT.name}
    )
    response = client.get(url)
    assert response.status_code == 200
    assert all(
        faq.service_type == ServiceType.FRACTIONAL_MANAGEMENT.value
        for faq in response.context["faqs"]
    )


def test_faqs_view_for_consultations(client, faqs):
    url = reverse("faqs", kwargs={"service_type": ServiceType.CONSULTATIONS.name})
    response = client.get(url)
    assert response.status_code == 200
    assert all(
        faq.service_type == ServiceType.CONSULTATIONS.value
        for faq in response.context["faqs"]
    )


def test_faqs_view_with_invalid_service_type(client):
    url = reverse("faqs", kwargs={"service_type": "INVALID_TYPE"})
    response = client.get(url)
    assert response.status_code == 404


def test_invalid_token_properties(mocker):
    mock_create_assessment = mocker.patch("enterprises.recaptcha.create_assessment")
    mock_create_assessment.return_value.token_properties.valid = False
    result = is_human("test_token", "test_action")
    assert result is False


def test_action_mismatch(mocker):
    mock_create_assessment = mocker.patch("enterprises.recaptcha.create_assessment")
    mock_create_assessment.return_value.token_properties.valid = True
    mock_create_assessment.return_value.token_properties.action = "wrong_action"
    result = is_human("test_token", "test_action")
    assert result is False


def test_score_below_threshold(mocker):
    mock_create_assessment = mocker.patch("enterprises.recaptcha.create_assessment")
    mock_create_assessment.return_value.token_properties.valid = True
    mock_create_assessment.return_value.token_properties.action = "test_action"
    mock_create_assessment.return_value.risk_analysis.score = 0.5
    result = is_human("test_token", "test_action")
    assert result is False


def test_all_checks_pass(mocker):
    mock_create_assessment = mocker.patch("enterprises.recaptcha.create_assessment")
    mock_create_assessment.return_value.token_properties.valid = True
    mock_create_assessment.return_value.token_properties.action = "test_action"
    mock_create_assessment.return_value.risk_analysis.score = 0.9
    result = is_human("test_token", "test_action")
    assert result is True
