import pytest
from google.auth.exceptions import MutualTLSChannelError

from enterprises.forms import SUBMISSION_CHAR_LIMIT, BadRequest, ContactForm


@pytest.fixture
def valid_data():
    return {
        "name": "John Doe",
        "reply_email": "john.doe@example.com",
        "submission": "Hello, World!",
    }


def test_valid_form_submission(mocker, valid_data):
    mock_is_human = mocker.patch("enterprises.forms.is_human")
    mock_is_human.return_value = True
    form = ContactForm(data=valid_data)
    assert form.is_valid()


def test_invalid_form_submission_length(mocker, valid_data):
    mock_is_human = mocker.patch("enterprises.forms.is_human")
    mock_is_human.return_value = True
    valid_data["submission"] = "x" * (SUBMISSION_CHAR_LIMIT + 1)
    form = ContactForm(data=valid_data)
    assert not form.is_valid()
    assert "submission" in form.errors


def test_valid_form_submission_empty_name_field(mocker, valid_data):
    mock_is_human = mocker.patch("enterprises.forms.is_human")
    mock_is_human.return_value = True
    valid_data["name"] = ""
    form = ContactForm(data=valid_data)
    assert form.is_valid()  # name is optional


def test_recaptcha_fail(mocker, valid_data):
    mock_is_human = mocker.patch("enterprises.forms.is_human")
    mock_is_human.return_value = False
    form = ContactForm(data=valid_data)
    with pytest.raises(BadRequest):
        form.is_valid()


def test_recaptcha_exception(mocker, valid_data):
    mock_is_human = mocker.patch("enterprises.forms.is_human")
    mock_is_human.side_effect = MutualTLSChannelError("Here's an exception")
    form = ContactForm(data=valid_data)
    assert not form.is_valid()
    assert "submission" in form.errors
