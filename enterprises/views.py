from django.conf import settings
from django.core.exceptions import BadRequest
from django.http.response import Http404
from django.shortcuts import render

from enterprises.forms import ContactForm
from enterprises.models import FrequentlyAskedQuestion, ServiceType
from enterprises.recaptcha import is_human


def index(request):
    return render(request, "enterprises/index.html")


def about(request):
    return render(request, "enterprises/about.html")


def contact(request):
    form = ContactForm()
    context = {"form": form, "SITE_KEY": settings.RECAPTCHA_SITE_KEY, "action": "contact"}
    if request.method == "POST":
        valid = False
        if "g-recaptcha-response" in request.POST:
            try:
                valid = is_human(request.POST["g-recaptcha-response"], "contact")
            except Exception as e:
                # TODO: log e
                form.add_error(
                    "submission",
                    "We are sorry, but we're experiencing some difficulties with our provider just now. Please "
                    "try again in a few minutes."
                )
                return render(request, "enterprises/contact.html", context=context)

        if not valid:
            raise BadRequest()

        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO: thank you page

    return render(request, "enterprises/contact.html", context=context)


def faqs(request, service_type):
    service_type_enum = getattr(ServiceType, service_type.upper(), None)
    if service_type_enum is None:
        raise Http404
    service_value = service_type_enum.value
    faqs = FrequentlyAskedQuestion.objects.filter(service_type=service_value).iterator()
    return render(
        request, "enterprises/faqs.html", {"faqs": faqs, "service_type": service_value}
    )
