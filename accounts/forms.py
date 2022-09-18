from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField, ReadOnlyPasswordHashField
from django import forms



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length= 16,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "이름(한글 가능)",
            "class": "loginbox"
        })
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            "placeholder": "비밀번호(6자 이상)",
            "class": "loginbox"
        })
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            "placeholder": "비밀번호 확인",
            "class": "loginbox"
        })
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        # 우선 지금 fields는 수정할게없으니 그대로
        fields = UserCreationForm.Meta.fields



class CustomUserChangeForm(UserChangeForm):
    email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "이메일",
            "class": "loginbox"
        })
    )

    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "이름",
            "class": "loginbox"
        })
    )
    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "성",
            "class": "loginbox"
        })
    )
    password = ReadOnlyPasswordHashField(
        label="",
        help_text=(
            '<a class="passwordbox" href="{}">비밀번호 변경</a>'
        ),
    )

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
        

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(label="ID", widget=forms.TextInput(attrs={
        "class": 'loginbox'
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "class": 'loginbox'
            }),
    )


        