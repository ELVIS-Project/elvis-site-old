from django.conf.urls import patterns, include, url, static
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns

from elvis.views.main import home
from elvis.views.piece import PieceList, PieceDetail
from elvis.views.corpus import CorpusList, CorpusDetail

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = []

urlpatterns += format_suffix_patterns(
    patterns('',
        url(r'^$', home, name='home'),
        url(r'^pieces/$', PieceList.as_view(), name="piece-list"),
        url(r'^piece/(?P<pk>[0-9]+)/$', PieceDetail.as_view(), name="piece-detail"),
        url(r'^corpora/$', CorpusList.as_view(), name="corpus-list"),
        url(r'^corpus/(?P<pk>[0-9]+)/$', CorpusDetail.as_view(), name="corpus-detail"),
        url(r'^composers/$', PieceList.as_view(), name="piece-list"),
        url(r'^composer/(?P<pk>[0-9]+)/$', PieceDetail.as_view(), name="piece-detail"),
        url(r'^movements/$', PieceList.as_view(), name="piece-list"),
        url(r'^movement/(?P<pk>[0-9]+)/$', PieceDetail.as_view(), name="piece-detail"),
    )
)


# Only add admin if it's enabled
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )


# For serving stuff under MEDIA_ROOT in debug mode only
# if settings.DEBUG:
#     urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
