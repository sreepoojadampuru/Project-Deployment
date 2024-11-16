from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('profile.html', views.profile, name='profile'),
    path('login.html', views.login, name='login'),
    path('logout.html', views.logout, name='logout'),
    path('reg.html', views.reg, name='sign up'),
    path('settings.html', views.settings, name='Settings'),
    path('he.html', views.he, name='Help'),
    path('editor.html', views.editor, name='Terminal'),
    path('about.html', views.about, name='About'),
    path('notes.html', views.notes, name='Notes'),
    path('execute.html', views.execute_code, name='execute_code'),  # Add your execute code view
    path('run_java.html', views.run_java_code, name='run_java_code'),
    path('success.html', views.profile, name='success'),

]



