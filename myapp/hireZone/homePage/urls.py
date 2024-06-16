from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('registerHire/', views.registerHire, name='registerHire'),
    path('registerSeeker/', views.registerSeeker, name='registerSeeker'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search_results, name='search'),
    path('home/', views.home, name='home'),
    path('seeker/<int:seeker_id>/', views.seeker_detail, name='seeker_detail'),
    path('seeker/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),
    path('booking/<int:seeker_id>/',views.booking,name='booking'),
    path('about',views.about,name='about'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
