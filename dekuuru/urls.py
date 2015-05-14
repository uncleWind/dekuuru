from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'dekuuru.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', 'dekuuro.views.testView', name='test'),
    url(r'^login/', 'dekuuro.views.loginView', name='login'),
    url(r'^createboard/', 'dekuuro.views.createBoardView', name='createBoard')
    url(r'^register/', 'dekuuro.views.registrationView', name='register'),
    url(r'^home/', 'dekuuro.views.mainPageView', name='home'),
    url(r'^board/(?P<boardTag>[a-zA-Z]+)/$', 'dekuuro.views.boardView', name='board'),
    url(r'^addimage/', 'dekuuro.views.addImageView', name='addImage'),
    url(r'^profiles/', 'dekuuro.views.profilesView', name='profiles'),
    url(r'^profile/', 'dekuuro.views.profileView', name='profile'),
    url(r'^board/(?P<boardTag>[a-zA-Z]+)/(?P<boardImageID>d+)/$', 'dekuuro.views.imageDetailsView', name='imageDetails'),
    url(r'^subscriptions/(?P<username>[a-zA-Z]+)/$', 'dekuuro.views.subscriptionsView', name='subscriptions'),
    url(r'^boardtags/(?P<boardTag>[a-zA-Z]+)/$', 'dekuuro.views.boardTagsView', name='boardTags'),
    url(r'^search/', 'dekuuro.views.searchView', name='search'),
    url(r'^inviteusers/(?P<boardTag>[a-zA-Z]+)/$', 'dekuuro.views.inviteUsersView', name='inviteUsers'),
    url(r'^userprofile/(?P<username>[a-zA-Z]+)/$', 'dekuuro.views.userProfileView,' name='userProfile'),
]
