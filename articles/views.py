
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article, Comment

# Create your views here.
def index(request):
    articles = Article.objects.all()
    
    context ={
        'articles': articles,
    }

    return render(request, 'articles/index.html', context)

# def new(request):
#     form = ArticleForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'articles/new.html', context)
@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save() # save()는 데이터에 저장도하는데 위에서 지정안하면 새로 객체도 만듬
            return redirect('articles:detail', article.pk)
    
    else:
        # NEW 처리하는곳 GET으로 요청들어왔을때임
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context) # 이러면 기존 작성한 내용도 그대로보존

@login_required
def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    #기존
    #article.username = request.user
    # => 객체임

    #수정후
    article.username = request.user.username
    article.count += 1
    article.save()
    comments = Comment.objects.filter(article_id=article_pk)#뭐야 이거필드명이아니었네?
    # 디비에 article_id들어가게좀 만들어주셈 저기에 안뜨네
    # 이제 풀수있겟음여기부턴? 필터란게있었구나 get은 한개만뽑아오는거라고
    # 들은거같음!ㅋㅋㅋ
    context = {
        'article': article,
        'comments': comments,

    }
    return render(request, 'articles/detail.html', context)

def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            article.delete()
            return redirect('articles:index')
    return redirect('articles:detail', article.pk)
    

# def edit(request, article_pk):
#     article = Article.objects.get(pk=article_pk)
#     form = ArticleForm(instance=article)
#     context = {
#         'form': form,
#         'article': article, # 이걸줘야 article.pk를 edit페이지에서 씀
#     }
#     return render(request, 'articles/edit.html', context)
@login_required
def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article, # 이걸줘야 article.pk를 edit페이지에서 씀
        'form': form,
    }
    return render(request, 'articles/update.html', context)



@login_required
def download(request):
    return render(request, 'articles/download.html')

def test(request):
    return render(request, 'articles/test.html')



def comment(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        comment = Comment()
        print(request.user.username)
        comment.username = request.user.username
        comment.content = request.POST.get('comment')
        comment.article_id = article_pk
        comment.save()
        return redirect('articles:detail', article.pk)
    return redirect('articles:detail', article.pk)

def upcount(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        article.up_count += 1
        article.save()
        return redirect('articles:detail', article.pk)
    return redirect('articles:detail', article.pk)


