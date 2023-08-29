from enterprises.recaptcha import is_human


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
