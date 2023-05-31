from django.shortcuts import render


def index(request):
    return render(request, "enterprises/index.html")


def about(request):
    return render(request, 'enterprises/about.html')


def lessons(request):
    return render(request, 'enterprises/lessons.html')


def business(request):
    return render(request, 'enterprises/business.html')


def performances(request):
    return render(request, 'enterprises/performances.html')


def research(request):
    return render(request, 'enterprises/research.html')


def contact(request):
    return render(request, 'enterprises/contact.html')
