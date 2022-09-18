from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm

# Create your views here.
def movies(request):
    movies = Movie.objects.all()

    context = {
        'movies': movies,
    }
    return render(request, 'movies/movies.html', context)


def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:movies')

    else:
        form = MovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/create.html', context)

def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)

    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)

def delete(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            movie.delete()
            return redirect('movies:movies')

    return redirect('movies:detail', movie.pk)

        