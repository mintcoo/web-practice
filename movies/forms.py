from django import forms
from movies.models import Movie


class MovieForm(forms.ModelForm):
    # header = forms.CharField(
    #     label='장르',
    #     widget=forms.Select(
    #         attrs={
    #             'choices': 'header_choices'
    #         }
    #     )
    # )
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'titlebox',
                'placeholder': ' 제목을 입력바람!'
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '간략한 영화내용!'
            }
        )
    )
    score = forms.FloatField(
        label='평점',
        widget=forms.NumberInput(
            attrs={
                'type': 'number',
                'min': '0',
                'max': '5',
                'step': '0.5',
            }
        )
    )
    release_date = forms.DateField(
        label='출시일',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )
    poster_url = forms.CharField(
        label='영화포스터',
        widget=forms.TextInput(
            attrs={
                'type': 'url',
                'placeholder': '영화 이미지주소를 입력'
                
            }
        )

    )

    class Meta:
        model = Movie
        fields = ('genre', 'title', 'score', 'content', 'release_date', 'poster_url')