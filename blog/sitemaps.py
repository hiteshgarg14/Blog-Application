from django.contrib.sitemaps import Sitemap
from blog.models import Post

# https://docs.djangoproject.com/en/1.10/ref/contrib/sitemaps/

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9 # maximum value is 1

    # The items() method returns the QuerySet of objects to include in this sitemap
    def items(self):
        return Post.published.all()

    """
    By default, Django calls the get_absolute_url() method on each object to retrieve its URL.
    If you want to specify the URL for each object, you can add a location method to your sitemap class.
    """

    # The lastmod method receives each object returned by items() and returns the last time the object was modified.
    def lastmod(self, obj):
        return obj.publish
