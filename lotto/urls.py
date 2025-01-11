from django.urls import path
from . import views

app_name = 'lotto'

urlpatterns = [
    path('', views.index, name='index'),  # 예시로 기본 페이지를 추가할 수 있습니다.
    path('buy/', views.buy_lotto, name='buy_lotto'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),
    path('draw/', views.draw_lotto, name='draw_lotto'),
]
