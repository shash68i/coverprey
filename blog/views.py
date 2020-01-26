from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.db.models.functions import Greatest
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Count
from taggit.models import Tag
from .models import Post, Comment
from .forms import CommentForm, MyCreateForm
from django.views.generic import (ListView,  
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                            )   


# class PostListView(LoginRequiredMixin, ListView):
#     login_url = '/login/'
#     model = Post
#     context_object_name = 'posts'
#     paginate_by = 4
#     template_name = 'blog/post_list.html'
#     ordering = ['-publish']


@login_required(login_url='/login/')
def PostListView(request, tag_slug=None):
    posts = Post.objects.order_by('-publish')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    # For searched posts
    if request.GET.get('q') is not None:
        query = request.GET.get('q')
        # search_vector = SearchVector('book_name', weight='A') + \
        #                 SearchVector('author_name',weight='A') + \
        #                 SearchVector('title',weight='A') + \
        #                 SearchVector('body',weight='B')
        # search_query = SearchQuery(query)

        # posts = Post.objects.annotate(rank=SearchRank(search_vector, search_query))\
        #                             .filter(rank__gte=0.3).order_by('-rank')
        posts = Post.objects.annotate(
            similarity=Greatest(
                TrigramSimilarity('book_name', query),
                TrigramSimilarity('author_name', query),
                TrigramSimilarity('title', query)
            )).filter(similarity__gte=0.1).order_by('-similarity')


    paginator = Paginator(posts, 4) # 4 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag':tag})


def PostDetailView(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)
    comments = post.post_comments.all()

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = user
            new_comment.save()
            return redirect('blog:post-detail', pk)
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids)\
                                  .exclude(pk=pk)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags','-publish')[:5]


    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'blog/post_detail.html', 
                            {'post': post,
                            'comments': comments,
                            'new_comment': new_comment,
                            'comment_form': comment_form,
                            'similar_posts': similar_posts,
                            'total_likes': post.total_likes(),
                            'is_liked': is_liked,})


class PostCreateView(LoginRequiredMixin, CreateView):
    # model = Post
    # fields = ['title', 'body', 'book_name', 'author_name', 'tags']
    form_class = MyCreateForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post-list')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def UserPostListView(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)


    paginator = Paginator(posts, 4) # 4 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)


    return render(request, 'blog/user_posts.html', {'posts':posts, 
                                                    'thisuser':user,
                                                    'page':page})


@login_required
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})