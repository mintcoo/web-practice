
from http.client import HTTPResponse
from re import A
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article, Comment, Upcheck

# Create your views here.
def index(request):
    articles = Article.objects.all()
    
    for article in articles:
        # 저기좀 다듬으면 ㅈ깔금ㅁ하게가능 아 이거 저 찾으면서 strftime 이거는 계속봤는데 이게 이렇게쓰면되는구나
        # ㅇㅇ 글고 아까 이거또 응용하면
        # print(article.created_at.time())
        # "2022-09-10 08:11:19.688436" -> 이시간을 타임스탬프화시키면
        # 53258902385902308 뭐이런게되는데
        # 이걸 
        # 하루만큼뺴는구나! ㅇㅋ 
        # 근데 1980부터 흐른거라햇자늠? millisecond단위고
        # 그럼 

        # A시간: 1초전
        # B시간: 10초전

        # A시간 - B시간은 몇일거같음?9인데 millisoecnd900ㅇ0ㅋ
        # 그럼
        # 두시간차의 값이 하루면 몇이되야할거같음?
        # 1분이면 몇일거같음? 저거 영그님 900맞나 ㅇㅇ1000이 1초니까
        # ㅇㅇ 그래서 1분이면 몇임60000
        # 정답! 1000 * 60
        # 1분 1000 * 60
        # 한시간 = 60분 = 1000* 60 * 60
        # 하루 = 1000 * 60 * 60 * 24
        # 이해됨? ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ
        # Article에는 글쓴시간이있음 
        # Article.createdAt 
        # 그리고 첫페이지목록접근하면 파이썬에선 time.time하면 현재시간얻을수있음
        # 그렇다면
        # 글쓴시간 A
        # 현재시간 B

        # B-A >= 1000 * 60 * 60 * 24 =>하루이상차이
        # B-A < 1000 * 60 * 60 * 24 => 하루이내캬
        # 근데 이게 원리인거고 무족권이해를해야되서설명한거고 이걸
        # 이제 사람들이 편하게쓰려고 라이브러리화를함
        # 그게이제 어디선가봣을법한
        # day(뭐이딴거일듯) 이런식으로아닐테지만 아무튼 시간입력하면
        # 차이구해줌 하루같은거 그거를 찾으면됨 이제 원리가 저렇게되는구나

        #이런식 와 이게또 이프문으로 처리가되네 와 이게 결합이 장난아니다
        article.test = article.날짜이쁘게(article.created_at)
        article.title = article.욕필터(article.title)

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
        comment.username = request.user.username
        comment.content = request.POST.get('comment')
        comment.article_id = article_pk
        comment.save()
        return redirect('articles:detail', article.pk)
    return redirect('articles:detail', article.pk)

# def upcheck(request, article_pk):
#     article = Article.objects.get(pk=article_pk)
#     context = {
#         'article': article,
#     }
#     return render(request, 'articles/upcheck.html', context)


def upcount(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    upchecks = Upcheck.objects.filter(article_id=article_pk,username=request.user.username)


    # 이 값(is_recommended)은 추천이 됬냐 체크하는 값
    is_recommended = len(upchecks) > 0
    # 이러면이해감? 이러면 갑자기 너무 익숙해짐 그럼 설명끝임 문제해결 다 끝난거 1,2,3 이게 영그님 그러면
    #아 근데 영그님 이게 길이잖음 그러면 저 필터조건에 걸ㄹ린 객체가 이제 최소 한놈있다는거 ㅇㅋ인데 그러면 헐 조건을 통과한놈이니까 그놈은 추천한놈이네

    # upchecks가 배열인건 암? 그 쿼리셋???ㅇㅋㅇㅋ 쿼리셋아 리스트
    # 배열ㅇ =ㅇ 링스ㅇㅇㅇ 리스ㅇ틍트! QuerySet[] 

    # 그럼  저런 배열형태의 내용의 갯수를 .__len__()하면 길이가 나옴 length의 약자임
    # 값이 3개면 3 ㅇ

    #이코드이해감? 영그님 저 사실 __ __ 이딴놈들 전혀몰겠음.. ㅠㅠ
    # 미쳤다..
    
    # 이미 추천됬으면 걍 디테일 redirect
    if is_recommended == True:
        print('추천됫으니 ㄲㅈ')
        return redirect('articles:detail', article.pk)
    
    #위에서 리턴했으니 여긴 무족권 is_recommended == False니까 else문 필요없음
    upcheck = Upcheck()
    upcheck.article_id = article.pk
    upcheck.username = request.user.username
    #dlrj?upcheck.up_check = 1 #이코드를 내까짠게아니라 원래잇어서 남은거라는뜻
    article.up_count += 1
    article.save()
    upcheck.save()
    return redirect('articles:detail', article.pk)

    


# def upcheck(request, article_pk):
#     upcheck = Upcheck.objects.get(article_id=article_pk)

            # upcheck = Upcheck()
            # upcheck.article_id = article.pk
            # upcheck.username = request.user.username
            # upcheck.save()