from django.contrib import admin
from .models import LottoTicket, LottoDraw
from .utils import generate_lotto_numbers

class LottoDrawAdmin(admin.ModelAdmin):
    list_display = ['draw_date', 'winning_numbers']

    def save_model(self, request, obj, form, change):
        if not change:  # 새로 생성된 경우에만 자동 번호 생성
            obj.winning_numbers = generate_lotto_numbers()
        super().save_model(request, obj, form, change)

admin.site.register(LottoDraw, LottoDrawAdmin)



class LottoTicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'numbers', 'purchase_date']

    def total_sales(self):
        return LottoTicket.objects.count()

    def total_winners(self):
        latest_draw = LottoDraw.objects.latest('draw_date')
        winning_numbers = set(map(int, latest_draw.winning_numbers.split(',')))
        winners = 0

        for ticket in LottoTicket.objects.all():
            ticket_numbers = set(map(int, ticket.numbers.split(',')))
            if ticket_numbers == winning_numbers:
                winners += 1

        return winners

admin.site.register(LottoTicket, LottoTicketAdmin)

# Register your models here.
