from django.shortcuts import redirect, render

def connect(request):
    return redirect('articles:index')

def test(request):
    return render(request, 'ttest.html')