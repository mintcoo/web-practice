from .models import Profile


def profile_processor(request):


    # 비로그인 유저 처리용 클래스 객체만듬
    first_profile = Profile()
    first_profile.icon_url = 'icon/anonymous.png'
    
    # 만약 익명 유저가 아니면
    is_anonymoususer = str(request.user) == 'AnonymousUser'
    if is_anonymoususer == False:
        [first_profile] = Profile.objects.filter(username=request.user.username) # 일치하는 이름으로 필터로 거름 (get은 없으면 오류)
                                                                                 # 필터는 리스트로 반환이라 [] 사용해 언팩하는거 알아두

    return {
        'profile': first_profile,
    }
