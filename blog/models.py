from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Post(models.Model):

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField(verbose_name='Content')
    book_name = models.CharField(max_length=250)
    author_name = models.CharField(max_length=100)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blog:post-detail',kwargs={'pk': self.pk})


class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,
                             related_name='post_comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE,
                               related_name='user_comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body