import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from enterprises.models import FrequentlyAskedQuestion, ServiceType

User = get_user_model()


@pytest.mark.django_db
def test_populate_database_no_user_data_in_db_and_is_populated():
    assert User.objects.exists() is False
    call_command("populate_database")
    assert User.objects.count() == 1
    assert User.objects.first().username == "admin"


@pytest.mark.django_db
def test_populate_database_no_faq_data_in_db_and_is_populated():
    assert FrequentlyAskedQuestion.objects.exists() is False
    call_command("populate_database")
    assert FrequentlyAskedQuestion.objects.count() > 0


@pytest.mark.django_db
def test_populate_database_user_data_already_in_db_so_is_not_populated():
    User.objects.create(username="admin", is_superuser=True, is_staff=True, is_active=True)
    assert User.objects.count() == 1
    call_command("populate_database")
    assert User.objects.count() == 1  # Nothing has been touched.


@pytest.mark.django_db
def test_populate_database_faq_data_already_in_db_so_is_not_populated():
    FrequentlyAskedQuestion.objects.create(
        question="Existing question",
        answer="Existing answer",
        ordering=0,
        service_type=ServiceType.FRACTIONAL_MANAGEMENT.value,
    )
    assert FrequentlyAskedQuestion.objects.count() == 1
    call_command("populate_database")
    assert FrequentlyAskedQuestion.objects.count() == 1  # Nothing has been touched.
    assert FrequentlyAskedQuestion.objects.first().question == "Existing question"
