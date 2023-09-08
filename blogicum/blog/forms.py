from blog.models import Comment, Post, User
from django import forms


class CommentForm(forms.ModelForm):
    '''Форма редактирования комментария'''
    class Meta:
        model = Comment
        fields = ('text',)
        widget = {
            'text': forms.Textarea({'rows': '3'})
        }


class PostForm(forms.ModelForm):
    '''Редактирование поста'''
    class Meta:
        model = Post
        exclude = ('author', 'created_at')
        widgets = {
            'text': forms.Textarea({'rows': '5'}),
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
            'email'
        )
