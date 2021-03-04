from django.urls import path
from .views import auth, testing

urlpatterns = [
    path('auth/test', auth.testApi, name='Test'),
    path('auth/keyVerification', auth.keyVerification, name='Verify vaccine/covid key'),
    path('auth/verifyIdentity', auth.identityVerification, name='Verify users identity'),
    path('auth/signup', auth.signup, name='Signup user'),
    path('auth/login', auth.loginUser, name='Login user'),
    path('auth/loginEmployee', auth.loginEmployee, name='Login employee'),
    path('auth/sendOneTimeText', auth.sendOneTimeText, name='Send one time password'),
    path('auth/verifyOneTimeText', auth.verifyOneTimeText, name='Verify one time password'),
    # 
    path('test', testing.testApi, name='Test user'),
    path('user/getProfile', testing.getProfile, name='Get user profile'),
    path('user/checkStatus', testing.checkStatus, name='Check user status'),

    # Employee
    path('employee/scanUser', testing.scanUser, name='Scans user QR code'),

]