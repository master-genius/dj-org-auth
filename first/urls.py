from django.urls import path
from . import views, orgviews
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('user/login/', views.LoginView.as_view()),
    path('user/register/', views.RegisterView.as_view()),
    path('user/logout/', views.user_logout),

    path('org/apitest', orgviews.api_test),

    #path('org/<str:org_id>/addcourse', orgviews.OrgCourseAdd.as_view()),
    path('org/<str:org_id>/addmember', orgviews.OrgAddMemberView.as_view()),

    path('org/<str:org_id>/login/', orgviews.OrgLoginView.as_view()),
    path('org/<str:org_id>/logout/', orgviews.org_user_logout),
    path('org/<str:org_id>/orgbind', orgviews.OrgBindPlatView.as_view()),
]

