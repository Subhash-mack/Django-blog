from django.urls import path,re_path,include
from .views import PostListView,PostDetailView,PostCreateView, PostNotification,PostUpdateView,PostDeleteView,UserPostListView,SearchView,LatestPostsView,CalendarView,PostNotification,RemoveNotification
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/',views.comment_post,name='comments'),
    path('comments/<int:id>',views.deletecomment,name='delete-comment'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('search/', SearchView.as_view(), name='search-results'),
    path('about/',views.about, name='blog-about'),
    path('like/',views.like_post,name='like-post'),
    path('blog/latest_posts',LatestPostsView.as_view(),name='latest-posts'),
    path('calendar/',CalendarView.as_view(),name='calendar'),
    path('event/new/',views.event,name='new-event'),
    path('event/edit/<int:id>/', views.event, name='edit-event'),
    path('notifications/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(),name='post-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),   

]

# path(r'calendar/$',CalendarView.as_view(),name='calendar'),
#     re_path(r'event/new/$',views.event,name='new-event'),
#     re_path(r'^event/edit/(?P<id>\d+)/$', views.event, name='edit-event'),