from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'dekuuru.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', 'dekuuro.views.testView', name='test'),
    url(r'^login/', 'dekuuro.views.loginView', name='login'),
    url(r'^createboard/', 'dekuuro.views.createBoardView', name='createBoard'),
]
