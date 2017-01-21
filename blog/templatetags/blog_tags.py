from django import template
from django.db.models import Count
from blog.models import Post

from django.utils.safestring import mark_safe
import markdown


register = template.Library()

"""
Restart the django server to register template tags with django.
"""

# Django will use the function's name as the tag name by default. @register.simple_tag(name='my_tag') .
@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    #default value is 5.
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

#https://docs.djangoproject.com/en/1.10/topics/db/aggregation/
# The notation for assignment template tags is {% template_tag as variable%}
@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


# https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/#writing-custom-template-filters
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
