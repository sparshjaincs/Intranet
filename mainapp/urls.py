from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('Leave/',views.Leave,name='Leave'),
    path('Heirarchy/',views.Heirarchy,name='Heirarchy'),
    path('Payroll/',views.Payroll,name='Payroll'),
    path('Documentation/',views.Documentation,name='Documentation'),
    path('Onboard/createmantis',views.createmantis,name='createmantis'),
    path('Track/',views.Track,name='Track'),
    path('dummyoffer/<token>', views.dummy, name="dummy"),
    #path('dummyoffer/',views.dummy,name='dummy'),
    path('nda',views.nda,name='nda'),

    path('Onboard/Delete',views.Delete,name='Delete'),
    path('Onboard/Bug_Issue',views.Bug,name='Bug_Issue'),
    path('Onboard/Send_Offer',views.sendoffer,name='Send_Offer')



]
