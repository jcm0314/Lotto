# urls.py
from django.urls import path
from . import views

app_name = 'lotto'

urlpatterns = [
    path('check-result/', views.check_results, name='check_results'),
    path('statistics/', views.statistics, name='statistics'),
    path('', views.home, name='home'),  # 홈 페이지 경로 추가
    path('draw/', views.draw_lotto, name='draw_lotto'),  # 관리자 추첨
    path('buy/', views.buy_lotto, name='buy_lotto'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
]

