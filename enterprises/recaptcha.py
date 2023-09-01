import logging

from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment

from evanduke import settings

logger = logging.getLogger(__file__)


def create_assessment(token: str) -> Assessment | None:
    """Create an assessment to analyze the risk of a UI action using the provided token."""
    project_id = "evan-duke-enterprises"
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = settings.RECAPTCHA_SITE_KEY
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    return client.create_assessment(request)


def is_human(token: str, recaptcha_action: str, threshold=0.85) -> bool:
    """Send the token off to Google for analysis and determine a verdict."""

    # Create an assessment
    assessment = create_assessment(token)

    # Check if the token is valid.
    if not assessment.token_properties.valid:
        logger.warning(
            f"The CreateAssessment call failed because the token was invalid for for the following reasons: "
            f"{str(assessment.token_properties.invalid_reason)}"
        )
        return False

    # Check if the expected action was executed.
    if assessment.token_properties.action != recaptcha_action:
        logger.warning(
            f"The action attribute in your reCAPTCHA tag does not match the action you are expecting to score"
            f"{assessment.token_properties.action} when {recaptcha_action} was expected."
        )
        return False
    else:
        # Get the risk score and the reason(s)
        # For more information on interpreting the assessment,
        # see: https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in assessment.risk_analysis.reasons:
            logger.info(f"Risk analysis reason: {reason}")
        logger.info(
            f"The reCAPTCHA score for this token is: {str(assessment.risk_analysis.score)}"
        )

    return assessment.risk_analysis.score >= threshold
