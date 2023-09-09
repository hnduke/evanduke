import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from enterprises.models import FrequentlyAskedQuestion, ServiceType

logger = logging.getLogger(__file__)


class Command(BaseCommand):
    """Automate the creation of essential data.

    This command will be run during each deployment.
    """

    def handle(self, *args, **options):
        logger.info("Initializing data.")
        admin_user, created = get_user_model().objects.update_or_create(
            username="admin",
            defaults={
                "is_superuser": True,
                "is_staff": True,
                "is_active": True,
            },
        )
        if created:
            admin_user.set_password(settings.ADMIN_INITIAL_PASSWORD)
            admin_user.email = settings.ADMIN_INITIAL_EMAIL
            admin_user.first_name = settings.ADMIN_INITIAL_FIRST_NAME
            admin_user.last_name = settings.ADMIN_INITIAL_LAST_NAME
            admin_user.save()

        if FrequentlyAskedQuestion.objects.count() == 0:
            faqs = [
                FrequentlyAskedQuestion(
                    question="What are Fractional Business Management Services?",
                    answer="The goal of our business is to help you get to the next level. You need someone to aid "
                    "in your operations or you need to hire your dream CEO but you are not quite there yet.",
                    ordering=0,
                    service_type=ServiceType.FRACTIONAL_MANAGEMENT.value,
                ),
                FrequentlyAskedQuestion(
                    question="How much work will you do in a week?",
                    answer="Our goal is to be very part time: we are going to spend only a portion of the week, "
                    "thereby making sure that your pocketbook doesn’t view us as a full time employee. The "
                    "total time commitment will be ten hours.",
                    ordering=1,
                    service_type=ServiceType.FRACTIONAL_MANAGEMENT.value,
                ),
                FrequentlyAskedQuestion(
                    question="Is there a contract?",
                    answer="Yes, there will be contracts laying out everything specifically as far as what we will "
                    "handle and what you can expect from us.",
                    ordering=2,
                    service_type=ServiceType.FRACTIONAL_MANAGEMENT.value,
                ),
                FrequentlyAskedQuestion(
                    question="How long will the contract for services be?",
                    answer="Every Contract is for a 6 month period, and it will come with the option to extend for "
                    "another 6 month period. If it becomes clear that the arrangement does not work well for "
                    "both parties, then the option of ending the contract exists as soon as the month comes to "
                    "a conclusion. For us, the goal is to be a short term solution. We want your business to "
                    "grow quickly so that you need to hire a full time person.",
                    ordering=3,
                    service_type=ServiceType.FRACTIONAL_MANAGEMENT.value,
                ),
                FrequentlyAskedQuestion(
                    question="How does payment work?",
                    answer="All bills must be paid on the first of the month for work that will be done during that "
                    "month. Bills that have not been paid within ten days of the start of the month will "
                    "automatically cancel the contract.",
                    ordering=4,
                    service_type=ServiceType.FRACTIONAL_MANAGEMENT.value,
                ),
                FrequentlyAskedQuestion(
                    question="What are your goals for my business?",
                    answer="Our goals will start to help you improve/develop processes, policies, and operating "
                    "procedures. Then, we will work towards successfully developing them and streamlining them. "
                    "At the end of the day, we want to make your business as efficient as possible.",
                    ordering=5,
                    service_type=ServiceType.FRACTIONAL_MANAGEMENT.value,
                ),
                FrequentlyAskedQuestion(
                    question="How much will this cost?",
                    answer="If our Fractional Business Management Services are a match, we will give you a quote at "
                    "that time.",
                    ordering=6,
                    service_type=ServiceType.FRACTIONAL_MANAGEMENT.value,
                ),
                FrequentlyAskedQuestion(
                    question="What am I paying for with the initial consultation fee?",
                    answer="You are paying for a one hour sit down meeting that will come with recommendations about "
                    "how you should improve your business. Any other consultations will come with the same fee, "
                    "with the possibility of additional recommendations.",
                    ordering=0,
                    service_type=ServiceType.CONSULTATIONS.value,
                ),
                FrequentlyAskedQuestion(
                    question="What will be in these recommendations? Will one of them contain Fractional Business "
                    "Services?",
                    answer="If it is clear that our Fractional Business Management Services will address your needs, "
                    "then it will be included in the recommendations, along with the package that we believe "
                    "best suits your needs.",
                    ordering=1,
                    service_type=ServiceType.CONSULTATIONS.value,
                ),
                FrequentlyAskedQuestion(
                    question="Will my consultation result in a recommendation of procuring your Fractional Business "
                    "Management Services?",
                    answer="It might, but it might not. At the end of the day, we view your business as unique, and "
                    "the solution needs to be modified to what your business needs. It is possible that we "
                    "recommend making some adjustments to your current business, we might recommend that you "
                    "consider acquiring some apps to help you streamline things. What we are most concerned "
                    "about is helping your business find the right solution for its needs.",
                    ordering=2,
                    service_type=ServiceType.CONSULTATIONS.value,
                ),
                FrequentlyAskedQuestion(
                    question="What will we cover in our consultation?",
                    answer="We will cover everything that you require. The goal is to help you be successful, not "
                    "sell any method of doing business or platform.",
                    ordering=3,
                    service_type=ServiceType.CONSULTATIONS.value,
                ),
                FrequentlyAskedQuestion(
                    question="What if I need something that you can’t address?",
                    answer="All consultations will be screened so as to make sure that we are not wasting your time "
                    "in covering things that we might not be able to help you with.",
                    ordering=4,
                    service_type=ServiceType.CONSULTATIONS.value,
                ),
                FrequentlyAskedQuestion(
                    question="Is there something between Fractional Business Management and Consultations?",
                    answer="We have a next level consulting package. For $400 a month, you get two sessions every "
                    "other week. The goal for each session is to sit down and assess the policies, processes "
                    "and procedures that you have and find ways to improve them. This package can be canceled "
                    "at any time, but payment is due on the first of the month. As with all of our contracts, "
                    "if we fail to receive payment by the 10th of the month, the contract will be voided.",
                    ordering=4,
                    service_type=ServiceType.CONSULTATIONS.value,
                ),
            ]
            FrequentlyAskedQuestion.objects.bulk_create(faqs)

        logger.info("Database initial population complete.")
