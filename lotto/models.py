from django.db import models
from django.contrib.auth.models import User

class LottoTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    numbers = models.CharField(max_length=50)  # 로또 번호 (예: "3, 7, 12, 19, 24, 31")
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.numbers}"

class LottoDraw(models.Model):
    draw_date = models.DateTimeField(auto_now_add=True)
    winning_numbers = models.CharField(max_length=50)

    def __str__(self):
        return f"Draw {self.id}: {self.winning_numbers}"

class LottoDraw(models.Model):
    draw_date = models.DateField()
    winning_numbers = models.CharField(max_length=255)
# Create your models here.
