from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from haystack.query import SearchQuerySet

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page and with page=posts
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    return render(request, 'blog/post/list.html', {'page':page, 'posts' : posts, 'tag':tag})

"""
class PostListView(ListView):

    # we could have specified model = Post and Django
    # would have built the generic Post.objects.all() QuerySet for us.

    queryset = Post.published.all()
    # The default variable is object_list
    context_object_name = 'posts'
    paginate_by = 3
    # default template, ListView will use blog/post_list.html .
    template_name = 'blog/post/list.html'
"""

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            new_comment = True
    else:
        new_comment = False
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',{'post':post, 'comments':comments,'similar_posts':similar_posts,
                                                    'comment_form':comment_form, 'new_comment':new_comment})

def post_share(request, post_id):
    # Reterived post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    cd = {}
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = '{0} ({1}) recommends you reading "{2}"'.format(cd['name'], cd['email_from'], post.title )
            message = 'Read "{0}" at {1}\n\n {2}\'s comments: {3}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'garg95hitesh@gmail.com', [cd['email_to']])

            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent, 'cd':cd})


def post_search(request):
    form = SearchForm()
    cd ={}
    results = None
    total_results = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            total_results = results.count()
    return render(request, 'blog/post/search.html', {'form':form, 'cd':cd,
                                                     'results':results, 'total_results':total_results})
