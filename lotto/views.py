from django.shortcuts import render, redirect
from .models import LottoTicket
from .utils import generate_lotto_numbers

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
    results = check_winning_numbers(request.user)
    return render(request, 'lotto/check_results.html', {'results': results})

# Create your views here.
