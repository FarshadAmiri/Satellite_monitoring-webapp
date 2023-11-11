from django.urls import path
from .views import *
# from .api.views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'

urlpatterns = [
    # path('', profile_view, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    # path('Profile/change?password', change_password_view.as_view(), name='change_password'),
    # path('profile/Update/<str:pk>', update_profile_view.as_view(), name='edit_info'),
    # path('Profile/delete?account?', delete_account_view, name='delete_account'),
    path('api-token-auth/', view=obtain_auth_token),
    # path('userinfo-api/', view=UserInfoAPI.as_view()),
    # path('user-logout-api/', view=UserLogoutAPI.as_view())
]