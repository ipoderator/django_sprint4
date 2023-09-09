from django import forms
from blog.models import User, Comment, Post

POST_FORM_INT: int = '5'
COMMENT_FORM_INT: int = '3'


class CommentForm(forms.ModelForm):
    '''Форма редактирования комментария'''
    class Meta:
        model = Comment
        fields = ('text',)
        widget = {
            'text': forms.Textarea({'rows': COMMENT_FORM_INT})
        }


class PostForm(forms.ModelForm):
    '''Редактирование поста'''
    class Meta:
        model = Post
        exclude = ('author', 'created_at')
        widgets = {
            'text': forms.Textarea({'rows': POST_FORM_INT}),
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ProfileForm(forms.ModelForm):
    '''Форма редактирования информации о пользователи'''
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
