from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import LottoTicket
from .models import LottoDraw
from .utils import generate_lotto_numbers
import random

# 로그인된 사용자만 접근할 수 있도록 데코레이터 추가
@login_required
def buy_lotto(request):
    if request.method == 'POST':
        # 로또 번호 자동 생성
        numbers = sorted(random.sample(range(1, 46), 6))

        # 로또 티켓 생성
        LottoTicket.objects.create(user=request.user, numbers=','.join(map(str, numbers)))

        return redirect('lotto:my_tickets')
    return render(request, 'lotto/buy_lotto.html')

def check_winning_numbers(user):
    latest_draw = LottoDraw.objects.latest('draw_date')
    user_tickets = LottoTicket.objects.filter(user=user)
    results = []

    for ticket in user_tickets:
        ticket_numbers = set(map(int, ticket.numbers.split(',')))
        winning_numbers = set(map(int, latest_draw.winning_numbers.split(',')))

        results.append({
            'ticket': ticket,
            'matched': len(ticket_numbers & winning_numbers),
            'is_winner': ticket_numbers == winning_numbers,
        })

    return results

def check_results(request):
    try:
        latest_draw = LottoDraw.objects.latest('draw_date')
    except LottoDraw.DoesNotExist:
        return render(request, 'lotto/no_draw.html', {'message': '아직 당첨 번호가 없습니다.'})

    user_tickets = LottoTicket.objects.filter(user=request.user)
    results = []

    for ticket in user_tickets:
        ticket_numbers = set(map(int, ticket.numbers.split(',')))
        winning_numbers = set(map(int, latest_draw.winning_numbers.split(',')))
        matched_numbers = ticket_numbers & winning_numbers
        is_winner = len(matched_numbers) == len(winning_numbers)

        results.append({
            'ticket': ticket.numbers,
            'matched_count': len(matched_numbers),
            'matched_numbers': sorted(matched_numbers),
            'is_winner': is_winner,
        })

    return render(request, 'lotto/check_results.html', {'results': results, 'latest_draw': latest_draw})

def home(request):
    return render(request, 'lotto/home.html')

def my_tickets(request):
    user_tickets = LottoTicket.objects.filter(user=request.user)  # 로그인한 사용자 티켓 조회
    return render(request, 'lotto/my_tickets.html', {'tickets': user_tickets})

def index(request):
    return render(request, 'lotto/index.html')

def draw_lotto(request):
    if request.user.is_staff:  # 관리자만 접근 가능
        # 1부터 45 사이의 숫자 중 6개를 랜덤으로 선택하여 정렬
        winning_numbers = sorted(random.sample(range(1, 46), 6))  
        # LottoDraw 모델에 당첨 번호 저장
        draw = LottoDraw.objects.create(winning_numbers=','.join(map(str, winning_numbers)))
        return redirect('lotto:my_tickets')  # 성공 시 티켓 페이지로 리디렉션
    else:
        return redirect('login')  # 관리자 아닐 시 로그인 페이지로 리디렉션

# views.py
def statistics(request):
    if not request.user.is_staff:
        return redirect('login')

    total_tickets = LottoTicket.objects.count()
    try:
        latest_draw = LottoDraw.objects.latest('draw_date')
    except LottoDraw.DoesNotExist:
        latest_draw = None

    if latest_draw:
        winning_numbers = set(map(int, latest_draw.winning_numbers.split(',')))
        winners = []
        for ticket in LottoTicket.objects.all():
            ticket_numbers = set(map(int, ticket.numbers.split(',')))
            matched_count = len(ticket_numbers & winning_numbers)
            winners.append((ticket, matched_count))

        winners = sorted(winners, key=lambda x: x[1], reverse=True)  # 매칭 개수로 정렬
    else:
        winners = []

    return render(request, 'lotto/statistics.html', {
        'total_tickets': total_tickets,
        'latest_draw': latest_draw,
        'winners': winners,
    })

# Create your views here.
