from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserAreaView, name='area'),
    path('login/', views.UserLoginView, name='login'),
    path('logout/', views.UserLogoutView, name='logout'),
    path('forgot-password/', views.ForgotPasswordView, name='forgot_password'),
    path('register/', views.UserRegisterView, name='register'),
    path('profile/', views.UserProfileView, name='profile'),
    path('adventures/', views.UserAdventuresView, name='adventures'),
    path('dashboard/', views.UserDashboardView, name='dashboard'),
    path('rewards/redeem/<int:reward_id>/', views.RedeemRewardView, name='redeem_reward'),
    path('account/delete/', views.RequestAccountDeletionView, name='request_deletion'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url='../profile/'
    ), name='password_change'),
] 