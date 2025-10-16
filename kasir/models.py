# kasir/models.py

from django.db import models
from django.utils import timezone # <-- Tambahkan import ini di paling atas

# ... (biarkan class Category dan Product yang sudah ada di sini) ...
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Kategori")
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nama Produk")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategori")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stok")
    def __str__(self):
        return self.name


# --- TAMBAHKAN DUA CLASS DI BAWAH INI ---

class Transaction(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Waktu Transaksi")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Harga")
    # cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Opsional jika ada login
    cash_received = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Uang Tunai", default=0)
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kembalian", default=0)
    
    def __str__(self):
        return f"Transaksi pada {self.created_at.strftime('%d-%m-%Y %H:%M')}"

class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.transaction.id}"