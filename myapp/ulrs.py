from django.contrib import admin
from django.urls import path
from . import views, views1, views2, views3
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views1.home, name='home'),
    path('truyen_id=<int:id>/', views1.doctruyen, name='doctruyen'),
    path('truyen_id=<int:id_truyen>/chuong=<int:id_chap>/', views1.view_docchuong, name='docchuong'),
    path('register/', views3.registerPage, name = 'register'),
    path('login/', views3.loginPage, name = 'login'),
    path('logout/', views3.dang_xuat, name = 'logout'),
    path('theloai=<str:theloai>/', views1.theloai, name='theloai'),
    path('theodoi/', views3.get_truyen_yeuthich, name = 'theodoi'),
    path('lichsu/', views3.get_lichsu, name='lichsu'),
    path('timkiem/', views1.timkiem, name='timkiem'),
    path('dangtruyen/', views2.dangtruyen, name='dangtruyen'),
    path('truyencuaban/', views2.truyencuaban, name='truyencuaban'),
    path('suatruyen_id=<int:id>/', views2.suatruyen, name='suatruyen'),
    path('themchap_truyen_id=<int:id>/', views2.themchap, name='themchap'),
    path('themchap_truyen_id=<int:id>/previewchap/', views2.previewchap, name='previewchap'),
    path('truyencuanhomdich/ten=<str:ten>/', views3.get_truyen_cua_nhomdich, name='truyencuanhomdich'),
    path('truyenmoicapnhat/', views1.truyenmoicapnhat, name='truyenmoicapnhat'),
] 
