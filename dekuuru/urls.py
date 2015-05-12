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
    url(r'^register/', 'dekuuro.views.registrationView', name='register'),
    url(r'^$', 'dekuuro.views.mainPageView', name='home'),
    url(r'^board/', 'dekuuro.views.boardView', name='board'),
    url(r'^addimage/', 'dekuuro.views.addImageView', name='addImage'),
    url(r'^profiles/', 'dekuuro.views.profilesView', name='profiles'),
    url(r'^profile/', 'dekuuro.views.profileView', name='profile'),
    url(r'^imagedetails/', 'dekuuro.views.imageDetailsView', name='imageDetails'),
    url(r'^subscriptions/', 'dekuuro.views.subscriptionsView', name='subscriptions'),
    url(r'^boardtags/', 'dekuuro.views.boardTagsView', name='boardTags'),
    url(r'^search/', 'dekuuro.views.searchView', name='search'),
    url(r'^inviteusers/', 'dekuuro.views.inviteUsersView', name='inviteUsers'),
    url(r'^userprofile/', 'dekuuro.views.userProfileView', name='userProfile'),
]
