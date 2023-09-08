from blog.models import Post
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import redirect


def post_all_query():
    '''Вернуть все посты'''
    query_set = (
        Post.objects.select_related(
            "category",
            "location",
            "author",
        )
        .annotate(comment_count=Count("comments"))
        .order_by("-pub_date")
    )
    return query_set


def post_published_query():
    '''Вернуть опубликованные посты'''
    query_set = post_all_query().filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )
    return query_set


class DataMixin:
    def dispatch(self, request, *args, **kwargs):
        """Отправляет изменения/удаления поста"""
        self.post_id = kwargs['pk']
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.post_id)
        return super().dispatch(request, *args, **kwargs)
