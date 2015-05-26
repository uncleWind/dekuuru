from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'dekuuru.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'dekuuro.views.loginView', name='login'),
    url(r'^logout/', 'dekuuro.views.logoutView', name='logout'),
    url(r'^createboard/', 'dekuuro.views.createBoardView', name='createBoard'),
    url(r'^register/', 'dekuuro.views.registrationView', name='register'),
    url(r'^$', 'dekuuro.views.mainPageView', name='home'),
    url(r'^board/(?P<boardTag>[a-zA-Z]+)/$', 'dekuuro.views.boardView', name='board'),
    url(r'^boards/', 'dekuuro.views.boardsView', name='boards'),
    url(r'^board/(?P<boardTag>[a-zA-Z]+)/addimage/', 'dekuuro.views.addImageView', name='addImage'),
    url(r'^profiles/', 'dekuuro.views.profilesView', name='profiles'),
    url(r'^profile/', 'dekuuro.views.profileView', name='profile'),
    url(r'^board/(?P<boardTag>[a-zA-Z]+)/(?P<boardImageID>[0-9]+)/$', 'dekuuro.views.imageDetailsView', name='imageDetails'),
    url(r'^subscriptions/(?P<username>[a-zA-Z]+)/$', 'dekuuro.views.subscriptionsView', name='subscriptions'),
    url(r'^boardtags/(?P<boardTag>[a-zA-Z]+)/$', 'dekuuro.views.boardTagsView', name='boardTags'),
    url(r'^boardtags/(?P<boardTag>[a-zA-Z]+)/edit/(?P<tagName>[a-zA-Z]+)/$', 'dekuuro.views.editTagView', name='editTag'),
    url(r'^boardtags/(?P<boardTag>[a-zA-Z]+)/remove/(?P<tagName>[a-zA-Z]+)/$', 'dekuuro.views.removeTagView', name='removeTag'),
    url(r'^imagetags/(?P<boardTag>[a-zA-Z]+)/(?P<imageID>[0-9]+)/remove/(?P<imageTag>[a-zA-Z]+)/$', 'dekuuro.views.removeImageTagView', name='removeImageTag'),
    url(r'^search/', 'dekuuro.views.searchView', name='search'),
    url(r'^inviteusers/(?P<boardTag>[a-zA-Z]+)/$', 'dekuuro.views.inviteUsersView', name='inviteUsers'),
    url(r'^userprofile/(?P<username>[a-zA-Z]+)/$', 'dekuuro.views.userProfileView', name='userProfile'),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
