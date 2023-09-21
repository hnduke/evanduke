import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.utils import timezone

from enterprises.admin import mark_as_read, mark_as_unread
from enterprises.models import ContactFormSubmission, FrequentlyAskedQuestion

User = get_user_model()


@pytest.fixture
def submission(db):
    return ContactFormSubmission.objects.create(
        name="Test User", read=False, submitted_at=timezone.localtime(), read_at=None
    )


@pytest.fixture
def faq_admin(db):
    from django.contrib.admin.sites import AdminSite

    from enterprises.admin import FrequentlyAskedQuestionAdmin

    return FrequentlyAskedQuestionAdmin(FrequentlyAskedQuestion, AdminSite())


@pytest.fixture
def contact_admin(db):
    from django.contrib.admin.sites import AdminSite

    from enterprises.admin import ContactFormSubmissionAdmin

    return ContactFormSubmissionAdmin(ContactFormSubmission, AdminSite())


@pytest.fixture
def request_factory():
    return RequestFactory()


def test_mark_as_read_action(admin_user, submission):
    queryset = ContactFormSubmission.objects.filter(id=submission.id)
    assert queryset.first().read is False

    mark_as_read(None, None, queryset)
    submission.refresh_from_db()
    assert submission.read is True


def test_mark_as_unread_action(admin_user, submission):
    queryset = ContactFormSubmission.objects.filter(id=submission.id)
    queryset.update(read=True)

    mark_as_unread(None, None, queryset)
    submission.refresh_from_db()
    assert submission.read is False


def test_change_view(admin_user, submission, contact_admin, request_factory):
    request = request_factory.get("/admin")
    request.user = admin_user

    object_id = submission.id
    extra_context = None

    contact_admin.change_view(request, str(object_id), extra_context=extra_context)
    submission.refresh_from_db()

    assert submission.read is True
    assert submission.read_at is not None


def test_has_add_permission(admin_user, contact_admin, request_factory):
    request = request_factory.get("/admin")
    request.user = admin_user

    result = contact_admin.has_add_permission(request)
    assert result is False
