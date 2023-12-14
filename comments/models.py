from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def total_rating(self):
        return self.likes.aggregate(models.Sum('value'))['value__sum'] or 0

    def calculate_thread_rating(self):
        # считаем популярность всей ветке через рекурсивный подсчет всех комментариев ниже уровнем
        rating = self.total_rating()
        for child in self.children.all():
            rating += child.calculate_thread_rating()
        return rating

    def __str__(self):
        return f'Comment by {self.user.username} - {self.timestamp}'


class Rate(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="likes")
    RAITING_CHOICES = (
        (1, "like"),
        (-1, "dislike"),
    )

    value = models.IntegerField(
        choices=RAITING_CHOICES)
