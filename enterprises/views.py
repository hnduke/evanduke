from django.shortcuts import render


def index(request):
    return render(request, "enterprises/index.html")


def about(request):
    return render(request, 'enterprises/about.html')


def contact(request):
    return render(request, 'enterprises/contact.html')
