from django.shortcuts import render

from enterprises.forms import ContactForm


def index(request):
    return render(request, "enterprises/index.html")


def about(request):
    return render(request, 'enterprises/about.html')


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'enterprises/contact.html', context={"form": form})
