from django.shortcuts import redirect

def connect(request):
    return redirect('articles:index')