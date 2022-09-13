from django import forms
from articles.models import Article

# class ArticleForm(forms.Form):
    # title = forms.CharField(max_length=10)
    # content = forms.CharField(widget=forms.Textarea)

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(
            attrs={
                'class': 'titlebox',
                'placeholder': '  제목을 입력바람!'
            }
        )
    )
    content = forms.CharField(
        label='Content',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '내용을 입력바람!'
            }
        )
    )

    class Meta:
        model = Article
        fields = ('header', 'title', 'content',)