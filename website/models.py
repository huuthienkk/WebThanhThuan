from django.db import models
from django.contrib.auth.models import User

class Tour(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class TourRegistration(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết với User
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)  # Liên kết với Tour
    registration_date = models.DateTimeField(auto_now_add=True)  # Ngày đăng ký

    @property
    def customer_name(self):
        return self.customer.username  # Hoặc self.customer.get_full_name() nếu bạn muốn tên đầy đủ
