from django.shortcuts import render
from django.http import HttpResponse

# Temporarily using index request for base.
def index(request):
    context_dict = {'heading': "Hello World"}
    return render(request, 'reviews/index.html', context=context_dict)
