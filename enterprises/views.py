from django.http.response import Http404
from django.shortcuts import render

from enterprises.forms import ContactForm
from enterprises.models import FrequentlyAskedQuestion, ServiceType


def index(request):
    return render(request, "enterprises/index.html")


def about(request):
    return render(request, "enterprises/about.html")


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "enterprises/contact.html", context={"form": form})


def faqs(request, service_type):
    service_type_enum = getattr(ServiceType, service_type.upper(), None)
    if service_type_enum is None:
        raise Http404
    service_value = service_type_enum.value
    faqs = FrequentlyAskedQuestion.objects.filter(service_type=service_value).iterator()
    return render(
        request, "enterprises/faqs.html", {"faqs": faqs, "service_type": service_value}
    )
