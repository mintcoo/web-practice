from .models import Usericon, Profile


def icon_processor(request):
    icons = Usericon.objects.all()

    return {
        'icons': icons,
    }

def profile_processor(request):
    profiles = Profile.objects.all()

    return {
        'profiles': profiles,
    }