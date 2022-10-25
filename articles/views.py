from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .forms import ArticleForm
from .models import Article, Comment, Itembox, Upcheck, Usericon, Colorbox
from .context_processors import Profile
from datetime import datetime 
import time
interval = 1

def get_page(request):
    global interval
    page = int(request.GET.get('page', 1))                      # 요청 페이지를 받아올때 인트값으로, 디폴트 1
    page_size = 10                                              # 보여줄 페이지의 개수
    page_end = page * page_size                                 # 아래에서 게시글을 페이지개수만큼 자를 변수
    page_start = page_end - page_size
    paginations = (len(Article.objects.all()) // page_size) +1  # 모든 게시글개수를 페이지 사이즈만큼 나누고 +1 만큼 페이지네이션 생성 
    paginations_size = 3                                        # 페이지네이션 사이즈 (html에도 값 바꿔주어야함)
    if page <= paginations_size:                                # 페이지네이션 사이즈 처리 구간 첫 1,2,3 구간일때
        interval = 1                                            
    if page != 1 and page % paginations_size == 1:              # 페이지가 1이아니고 페이지네이션 사이즈로 나눈 나머지 1일때 (즉 현재설정으론 4페이지)
        interval = page                                         # 글로벌 interval을 page값으로 할당 (아래에 range범위 바꿔서 다시 렌더링 해야함)
    # print('&&$$$$$$$$$$$$$$$$',paginations)
    articles = Article.objects.all()[::-1]
    articles = articles[page_start:page_end]                    # 현재 페이지 사이즈 10개만큼 잘라서 렌더링해야함

    time_now = int(time.mktime(datetime.now().date().timetuple()))      # 중요!! 현재시간의 현재날짜 00시 기준의 값을 타임스탬프로 받아와야함!

    for article in articles:
        # article.test = article.날짜이쁘게(article.created_at)
        article.title = article.욕필터(article.title)
        article_time = int(time.mktime(article.created_at.timetuple()))     # 게시글 작성시간을 타임스탬프화 시키고
        article.time_slice = article_time - time_now + 32400                # 중요!! 오늘날짜 00시 기준값에서 작성시간 빼고 32400(시차)만큼 더해준값 음수면 넘어가게..(이 값으로 index페이지에서 사용)
        # print('@@@@@@', article.time_slice)                                                                        

        if article.comment_count == 0:
            article.comment_count = ''          # 코멘트 0 이면 빈칸 
        else:
             article.comment_count = f' [{ article.comment_count }]'    
    
    # articles for문돌면서 거기에 profile꽂아주려함
    # 그럼 기존 html쪽 for문에서 article.profile.icon_url하믄대니까
    # print('aa',usernames)


    # 인기글 정렬하는거 order_by를 통해 정렬 '-'을 통해 많은순
    article_popular = Article.objects.all().order_by('-up_count')[:3]  

    for popular in article_popular:
        popular.title = popular.욕필터(popular.title)
        popular_time = int(time.mktime(popular.created_at.timetuple()))    
        popular.time_slice = popular_time - time_now + 32400     
        if popular.comment_count == 0:
            popular.comment_count = ''
        else:
             popular.comment_count = f' [{ popular.comment_count}]'

    #lambda쓰는거조금씩이제 해보자!!
    usernames = list(map(lambda x:x.username, articles))
    usernames2 = list(map(lambda x:x.username, article_popular))
    # print('@@@',usernames)
    # print('@@@',usernames2)
    # 여기서 usernames로 profile끌어오면 profiles들어잇고
    profiles = Profile.objects.filter(username__in=usernames)
    profiles2 = Profile.objects.filter(username__in=usernames2)
    

    for article in articles:
        # profiles이거안에 article.username이랑 profiles중의 profile.username이같은거 무족권있을꺼고
        # 그걸 article.profile = profile 해서넣어준다는뜻 데이터베이스에 지정한 필드값들만 이렇게 끌고올수있는게 아니다!
        for profile in profiles:
            if profile.username == article.username :
                article.profile = profile.icon_url
                article.id_color = profile.id_color
                article.title_color = profile.title_color

    for article in article_popular:                 
        for pro in profiles2:
            if pro.username == article.username :
                article.profile = pro.icon_url
                article.id_color = pro.id_color
                article.title_color = pro.title_color

    context ={
        'articles': articles,
        'article_popular': article_popular,
        'range': range(interval, paginations + 1),                      # 여기 range를 전달함으로써 구간만큼 페이지네이션 버튼 생성
        'interval': interval,
        'interval_2': interval + paginations_size,
        'paginations_size': paginations_size,
    }
    context = serializers.serialize("json", articles)
    return HttpResponse(context, content_type='application/json')
    #return JsonResponse(context,safe=False)

# Create your views here.
def index(request):
    global interval
    page = int(request.GET.get('page', 1))                      # 요청 페이지를 받아올때 인트값으로, 디폴트 1
    page_size = 10                                              # 보여줄 페이지의 개수
    page_end = page * page_size                                 # 아래에서 게시글을 페이지개수만큼 자를 변수
    page_start = page_end - page_size
    paginations = (len(Article.objects.all()) // page_size) +1  # 모든 게시글개수를 페이지 사이즈만큼 나누고 +1 만큼 페이지네이션 생성 
    paginations_size = 3                                        # 페이지네이션 사이즈 (html에도 값 바꿔주어야함)
    if page <= paginations_size:                                # 페이지네이션 사이즈 처리 구간 첫 1,2,3 구간일때
        interval = 1                                            
    if page != 1 and page % paginations_size == 1:              # 페이지가 1이아니고 페이지네이션 사이즈로 나눈 나머지 1일때 (즉 현재설정으론 4페이지)
        interval = page                                         # 글로벌 interval을 page값으로 할당 (아래에 range범위 바꿔서 다시 렌더링 해야함)
    # print('&&$$$$$$$$$$$$$$$$',paginations)
    articles = Article.objects.all()[::-1]
    articles = articles[page_start:page_end]                    # 현재 페이지 사이즈 10개만큼 잘라서 렌더링해야함

    time_now = int(time.mktime(datetime.now().date().timetuple()))      # 중요!! 현재시간의 현재날짜 00시 기준의 값을 타임스탬프로 받아와야함!

    for article in articles:
        # article.test = article.날짜이쁘게(article.created_at)
        article.title = article.욕필터(article.title)
        article_time = int(time.mktime(article.created_at.timetuple()))     # 게시글 작성시간을 타임스탬프화 시키고
        article.time_slice = article_time - time_now + 32400                # 중요!! 오늘날짜 00시 기준값에서 작성시간 빼고 32400(시차)만큼 더해준값 음수면 넘어가게..(이 값으로 index페이지에서 사용)
        # print('@@@@@@', article.time_slice)                                                                        

        if article.comment_count == 0:
            article.comment_count = ''          # 코멘트 0 이면 빈칸 
        else:
             article.comment_count = f' [{ article.comment_count }]'    
    
    # articles for문돌면서 거기에 profile꽂아주려함
    # 그럼 기존 html쪽 for문에서 article.profile.icon_url하믄대니까
    # print('aa',usernames)


    # 인기글 정렬하는거 order_by를 통해 정렬 '-'을 통해 많은순
    article_popular = Article.objects.all().order_by('-up_count')[:3]  

    for popular in article_popular:
        popular.title = popular.욕필터(popular.title)
        popular_time = int(time.mktime(popular.created_at.timetuple()))    
        popular.time_slice = popular_time - time_now + 32400     
        if popular.comment_count == 0:
            popular.comment_count = ''
        else:
             popular.comment_count = f' [{ popular.comment_count}]'

    #lambda쓰는거조금씩이제 해보자!!
    usernames = list(map(lambda x:x.username, articles))
    usernames2 = list(map(lambda x:x.username, article_popular))
    # print('@@@',usernames)
    # print('@@@',usernames2)
    # 여기서 usernames로 profile끌어오면 profiles들어잇고
    profiles = Profile.objects.filter(username__in=usernames)
    profiles2 = Profile.objects.filter(username__in=usernames2)
    

    for article in articles:
        # profiles이거안에 article.username이랑 profiles중의 profile.username이같은거 무족권있을꺼고
        # 그걸 article.profile = profile 해서넣어준다는뜻 데이터베이스에 지정한 필드값들만 이렇게 끌고올수있는게 아니다!
        for profile in profiles:
            if profile.username == article.username :
                article.profile = profile.icon_url
                article.id_color = profile.id_color
                article.title_color = profile.title_color

    for article in article_popular:                 
        for pro in profiles2:
            if pro.username == article.username :
                article.profile = pro.icon_url
                article.id_color = pro.id_color
                article.title_color = pro.title_color

    context ={
        'articles': articles,
        'article_popular': article_popular,
        'range': range(interval, paginations + 1),                      # 여기 range를 전달함으로써 구간만큼 페이지네이션 버튼 생성
        'interval': interval,
        'interval_2': interval + paginations_size,
        'paginations_size': paginations_size,
    }
    
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save() # save()는 데이터에 저장도하는데 위에서 지정안하면 새로 객체도 만듬
            article.username = request.user.username    # 따로해주는 이유는 지금 article.username은 디폴트값이 익명으로 되어있다
            article.save()
            request.user.point += 300
            request.user.save()

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
    profi = Profile.objects.get(username=article.username)
    #기존
    #article.username = request.user
    # => 객체임
    article.count += 1
    article.save()
    if article.username != '익명':
        article_user = User.objects.get(username=article.username)
        article.point = article_user.point

    comments = Comment.objects.filter(article_id=article_pk)
    usernames = list(map(lambda x:x.username, comments))
    # print('@@@',usernames)
    profiles = Profile.objects.filter(username__in=usernames)
    

    for comment in comments:
        # profiles이거안에 article.username이랑 profiles중의 profile.username이같은거 무족권있을꺼고
        # 그걸 article.profile = profile 해서넣어준다는뜻 데이터베이스에 지정한 필드값들만 이렇게 끌고올수있는게 아니다!
        for profile in profiles:
            if profile.username == comment.username :
                comment.profile = profile.icon_url
                comment.name_color = profile.id_color
                comment.title_color = profile.title_color


    context = {
        'article': article,
        'comments': comments,
        'profi': profi,

    }
    return render(request, 'articles/detail.html', context)

def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user.is_authenticated:
        if request.method == 'POST' and request.user.username == article.username:
            article.delete()
            return redirect('articles:index')
    return redirect('articles:detail', article.pk)
    

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
        'article': article, # 이걸줘야 article.pk를 edit페이지에서 씀!!
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
        article.comment_count += 1
        article.save()
        request.user.point += 100
        request.user.save()
        return redirect('articles:detail', article.pk)
    return redirect('articles:detail', article.pk)

def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        if comment.username == request.user.username:
            comment.delete()
            article.comment_count -= 1
            article.save()
            return redirect('articles:detail', article.pk)
    return redirect('articles:detail', article.pk)


def upcount(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    # 필터를 이용해 조건을 2개 걸었음! (특히 유저네임이 요청한 유저인지가 중요)
    upchecks = Upcheck.objects.filter(article_id=article_pk,username=request.user.username)


    # 이 값(is_recommended)은 추천이 됬냐 체크하는 값
    is_recommended = len(upchecks) > 0

    # 이미 추천됬으면 걍 디테일 redirect
    if is_recommended == True:
        return redirect('articles:detail', article.pk)
    
    #위에서 리턴했으니 여긴 무족권 is_recommended == False니까 else문 필요없음
    upcheck = Upcheck()
    upcheck.article_id = article.pk
    upcheck.username = request.user.username
    upcheck.save()
    article.up_count += 1
    article.save()
    request.user.point += 50
    request.user.save()
    return redirect('articles:detail', article.pk)

    
def search(request):
    q = request.GET.get('q')                # 우선 사용자가 검색한 값 q에 담긴값을 받아온다
    if q == '':                             # 빈칸을 검색했을때 처리
        context = {
        'q': q,
        } 
        return redirect('articles:index')
    
        
    articles = Article.objects.filter(title__icontains=q)               # 필터로 icontains=q 를 통해서 검색한 q가 제목에 포함된것 전부가져옴
    for article in articles:
        article.title = article.욕필터(article.title)
        if article.comment_count == 0:
            article.comment_count = ''
        else:
             article.comment_count = f' [{ article.comment_count}]'

    context = {
        'articles': articles,
    } 
    return render(request, 'articles/search.html', context)             # 검색결과로 새로 렌더링

@login_required
def pointshop(request):
    icons = Usericon.objects.all().order_by('price')
    itembox = Itembox.objects.filter(username=request.user.username)
    colorbox = Colorbox.objects.filter(username=request.user.username)
    user_icon_id = list(map(lambda x:x.icon_id, itembox))
    user_color = list(map(lambda x:x.color, colorbox))

    color_list = {'Black': 1000, 'Red': 1000, 'Blue': 1000, 'Green': 1000, 'Grey': 1500, 'Purple': 1500, 'Gold': 1500, 'Fuchsia': 2000, 'Maroon': 2500,
    'Lime': 2500, 'Navy': 2500, 'Chocolate': 2500, 'Slateblue': 3000, 'Teal': 3000, 'Skyblue': 4000, 'Pink': 4000, 'Cornflowerblue': 5000, 'Crimson': 5000, 'Steelblue': 5000,
    'Lavender': 7000, 'Snow': 7777,
    }
    
    context = {
        'icons': icons,
        'useritems': user_icon_id,
        'color_list': color_list,
        'usercolors': user_color,
    }

    return render (request, 'articles/pointshop.html', context)

@login_required
def icon_buy(request, icon_id, icon_price):
    if request.method == 'POST':
        request.user.point -= icon_price
        request.user.save()
        itembox = Itembox()
        itembox.username = request.user.username
        itembox.icon_id = icon_id
        itembox.save()
        return redirect('articles:pointshop')
    else:
        print('POST 요청아님')
    return redirect('articles:pointshop')

@login_required
def color_buy(request, color_name, color_price):
    if request.method == 'POST':
        request.user.point -= color_price
        request.user.save()
        colorbox = Colorbox()
        colorbox.username = request.user.username
        colorbox.color = color_name
        colorbox.save()
        return redirect('articles:pointshop')
    else:
        print('POST 요청아님')
    return redirect('articles:pointshop')

@login_required
def profile(request):
    icons = Usericon.objects.all()
    itembox = Itembox.objects.filter(username=request.user.username)
    colorbox = Colorbox.objects.filter(username=request.user.username)
    # user_icon_list = list(map(lambda x:x.icon_id, itembox))
    for icon in icons:
        for item in itembox:
            if item.icon_id == icon.icon_id:
                item.url = icon.url
    
    context = {
        'iconlist': itembox,
        'colorlist': colorbox,
    }

    return render(request, 'articles/profile.html', context)

@login_required
def icon_setting(request, icon_id):
    if request.method == 'POST':
        icon = Usericon.objects.get(icon_id=icon_id)
        profile = Profile.objects.get(username=request.user.username)
        profile.icon_id = icon_id
        profile.icon_url = icon.url
        profile.save()
        return redirect('articles:profile')
    else:
        return redirect('articles:profile')

@login_required
def color_username(request, color_name):
    if request.method == 'POST':
        profile = Profile.objects.get(username=request.user.username)
        profile.id_color = color_name
        profile.save()
        return redirect('articles:profile')
    else:
        return redirect('articles:profile')

@login_required
def color_title(request, color_name):
    if request.method == 'POST':
        profile = Profile.objects.get(username=request.user.username)
        profile.title_color = color_name
        profile.save()
        return redirect('articles:profile')
    else:
        return redirect('articles:profile')

