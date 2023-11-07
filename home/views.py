from django.http import HttpResponse

def index(request):
    return HttpResponse('This is a Django REST API meant to serve a React web app.')