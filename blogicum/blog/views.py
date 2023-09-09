from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count

from blog.models import Category, Comment, Post
from blog.forms import CommentForm, PostForm, ProfileForm
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from blog.utils import (
    post_all_query,
    post_published_query,
    DataMixin,
)

CURRENT_TIME = timezone.now()


class MainPostListView(ListView):
    '''Главная страница'''
    model = Post
    template_name = 'blog/index.html'
    queryset = post_published_query()
    paginate_by = 10


class ProfileLoginView(LoginView):
    def get_success_url(self):
        url = reverse(
            'blog:profile',
            args=(self.request.user.get_username(),)
        )
        return url


class EditProfileUserView(LoginRequiredMixin, UpdateView):
    '''Изменение профиля пользователя'''
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        username = self.request.user
        return reverse('blog:profile', kwargs={'username': username})


class UserPostsListView(MainPostListView):
    '''Информация о пользователе'''
    template_name = 'blog/profile.html'
    author = None

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        return self.get_object().posts.all().annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return context


class PostListView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        query_set = post_all_query().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
        return query_set


class PostCreateView(LoginRequiredMixin, CreateView):
    '''Создание поста'''
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        '''Проверка валидности формы'''
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        '''Получение адреса'''
        username = self.request.user
        return reverse(
            'blog:profile',
            kwargs=({'username': username})
        )


class PostUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        '''Получение адреса'''
        url = reverse('blog:post_detail', args=(self.post_id,))
        return url


class PostDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'


class PostDetailView(DetailView):
    '''Страница выбранного поста'''
    model = Post
    template_name = "blog/detail.html"
    post_data = None

    def get_queryset(self):
        self.post_data = get_object_or_404(Post, pk=self.kwargs["pk"])
        if self.post_data.author == self.request.user:
            return post_all_query().filter(pk=self.kwargs["pk"])
        return post_published_query().filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context["flag"] = True

        context['comments'] = (
            self.object.comments.select_related(
                'author'
            )
        )
        return context

    def check_post_data(self):
        '''Вернуть результат проверки поста'''
        return all(
            (
                self.post_data.is_published,
                self.post_data.pub_date,
                self.post_data.category.is_published,
            )
        )


@login_required
def category_posts(request, category_slug):
    '''Отображение по категории постов'''
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    category_list = category.posts.filter(
        pub_date__lte=CURRENT_TIME,
        is_published=True,
    ).select_related(
        'category',
    )
    paginator = Paginator(category_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, 'blog/category.html', context)


@login_required
def add_comment(request, pk):
    '''Добавление комментария'''
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, comment_id, post_id):
    '''Изменение комментария'''
    instance = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    form = CommentForm(request.POST or None, instance=instance)
    if instance.author != request.user:
        return redirect('blog:post_detail', pk=post_id)
    context = {
        'form': form,
        'comment': instance
    }

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, comment_id, post_id):
    '''Удаление комментария'''
    instance = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if instance.author != request.user:
        return redirect('blog:post_detail', pk=post_id)
    context = {'comment': instance}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html', context)
