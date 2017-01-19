from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm

"""
def post_list(request):
    object_list = Post.published.all()
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
    return render(request, 'blog/post/list.html', {'page':page, 'posts' : posts})
"""

class PostListView(ListView):
    """
    we could have specified model = Post and Django
    would have built the generic Post.objects.all() QuerySet for us.
    """
    queryset = Post.published.all()
    # The default variable is object_list
    context_object_name = 'posts'
    paginate_by = 3
    # default template, ListView will use blog/post_list.html .
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html',{'post':post})

def post_share(request, post_id):
    # Reterived post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form})    
