from django.conf import settings
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from enterprises.forms import ContactForm
from enterprises.models import (
    ContactFormSubmission,
    FrequentlyAskedQuestion,
    ServiceType,
)


def index(request):
    return render(request, "enterprises/index.html")


def about(request):
    return render(request, "enterprises/about.html")


class ContactView(FormView):
    template_name = "enterprises/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("thank-you")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["SITE_KEY"] = settings.RECAPTCHA_SITE_KEY
        context["action"] = self.form_class.action
        return context

    def form_valid(self, form):
        submission = form.save()
        self.request.session["submission-uuid"] = str(submission.id)
        return super().form_valid(form)


def faqs(request, service_type):
    service_type_enum = getattr(ServiceType, service_type.upper(), None)
    if service_type_enum is None:
        raise Http404
    service_value = service_type_enum.value
    faqs = FrequentlyAskedQuestion.objects.filter(service_type=service_value).iterator()
    return render(
        request, "enterprises/faqs.html", {"faqs": faqs, "service_type": service_value}
    )
