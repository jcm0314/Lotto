from django.shortcuts import render, redirect
from .models import LottoTicket
from .models import LottoDraw
from .utils import generate_lotto_numbers
import random

def buy_lotto(request):
    if request.method == "POST":
        numbers = generate_lotto_numbers()
        LottoTicket.objects.create(user=request.user, numbers=numbers)
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
    # 최근 추첨 번호 가져오기
    try:
        latest_draw = LottoDraw.objects.latest('draw_date')
    except LottoDraw.DoesNotExist:
        return render(request, 'lotto/no_draw.html')  # 추첨이 아직 없는 경우

    user_tickets = LottoTicket.objects.filter(user=request.user)  # 사용자의 티켓을 가져옴
    results = []

    for ticket in user_tickets:
        ticket_numbers = set(map(int, ticket.numbers.split(',')))
        winning_numbers = set(map(int, latest_draw.winning_numbers.split(',')))
        matched = ticket_numbers & winning_numbers
        is_winner = ticket_numbers == winning_numbers

        results.append({
            'ticket': ticket,
            'matched': len(matched),
            'is_winner': is_winner,
            'matched_numbers': sorted(list(matched)),
        })

    return render(request, 'lotto/check_results.html', {'results': results})


def home(request):
    return render(request, 'lotto/home.html')

def my_tickets(request):
    return render(request, 'lotto/my_tickets.html')

def index(request):
    return render(request, 'lotto/index.html')

def draw_lotto(request):
    if request.user.is_staff:
	winning_numbers = sorted(random.sample(range(1, 46), 6))
	draw = LottoDraw.objects.create(winning_numbers','.join(map(str, winning_numbers)))
	return redirect('lotto:my_tickets')
    else:
	return redirect('login')

def statistics(request):
    total_tickets = LottoTicket.objects.count()  # 총 티켓 판매량
    latest_draw = LottoDraw.objects.latest('draw_date')  # 최근 추첨 정보
    total_winners = LottoTicket.objects.filter(
        numbers__in=[latest_draw.winning_numbers]).count()  # 당첨된 티켓 수
    return render(request, 'lotto/statistics.html', {
        'total_tickets': total_tickets,
        'total_winners': total_winners,
        'latest_draw': latest_draw,
    })
# Create your views here.
