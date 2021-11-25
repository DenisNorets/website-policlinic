from django.urls import path
from . import views
from django.http import FileResponse

app_name = 'pages'
urlpatterns = [
    path('main/', views.main, name='main'),
    path('main/<str:name>/', views.main , name = 'main'),
    path('shedule/', views.shedule , name = 'shedule'),
    path('contacts/', views.contacts , name = 'contacts'),
    path('test/', views.test, name='test'),
    path('appointment/', views.appointment_view, name='appointment'),
    path('appointment/<int:day_id>/', views.appointment_view, name='appointment_by_id'),
    path('info/', views.info, name='info'),
    path('search/', views.search, name='search'),
    path('update/<int:app_id>/', views.update, name='update'),
    path('refuse/<int:app_id>/', views.refuse, name='refuse'),
    path('search/<int:app_id>/', views.search , name='search'),
    #path('main/', views.appo, name='test_post'),
]