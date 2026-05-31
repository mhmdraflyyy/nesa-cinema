from django.db import models
from booking.models import Tiket 

class Payment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    METHOD_CHOICES = (
        ('CREDIT_CARD', 'Credit Card'),
        ('E_WALLET', 'E-Wallet'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    )

    # 2. Ubah relasi dari Booking menjadi Tiket
    tiket = models.ForeignKey(Tiket, on_delete=models.CASCADE, related_name='payments', help_text="Pesanan tiket yang dibayar")
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total harga tiket")
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='E_WALLET')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 3. Sesuaikan dengan field kode_booking yang ada di model Tiket kamu
        return f"Payment #{self.id} - Tiket {self.tiket.kode_booking} - Rp {self.amount} ({self.status})"