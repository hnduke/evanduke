import pytest
from django.contrib.auth import get_user_model

from enterprises.models import FrequentlyAskedQuestion, ServiceType

User = get_user_model()


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


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser("admin", "admin@example.com", "password")
