# kasir/models.py

from django.db import models
from django.utils import timezone
from django.db.models import F, Sum

# ======================================================================
# PILAR 1: DAFTAR BAHAN (INVENTARIS)
# ======================================================================

class Ingredient(models.Model):
    """
    Model ini menyimpan semua item inventaris: bahan baku, bahan setengah jadi,
    dan bahan habis pakai (packaging, dll).
    """
    class IngredientType(models.TextChoices):
        BAHAN_BAKU = 'BB', 'Bahan Baku'
        BAHAN_SETENGAH_JADI = 'BSJ', 'Bahan Setengah Jadi'
        BAHAN_HABIS_PAKAI = 'BHP', 'Bahan Habis Pakai'

    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Bahan")
    type = models.CharField(max_length=3, choices=IngredientType.choices, verbose_name="Tipe Bahan")
    unit = models.CharField(max_length=20, verbose_name="Satuan Unit", help_text="Contoh: gram, ml, pcs")
    stock = models.FloatField(default=0, verbose_name="Stok Saat Ini")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga Modal per Unit")

    def __str__(self):
        return f"{self.name} ({self.stock} {self.unit})"

# ======================================================================
# MODIFIKASI: MODEL PRODUK (MENU)
# ======================================================================

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nama Produk")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Kategori")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga Jual")
    # Field 'stock' kita hapus dari sini, karena stok sekarang ada di level bahan baku
    
    def __str__(self):
        return self.name

    # Fungsi untuk menghitung COGS (Harga Pokok) per produk
    def calculate_cogs(self):
        cogs = self.recipes.aggregate(
            total_cost=Sum(F('ingredient__cost_per_unit') * F('quantity'))
        )['total_cost'] or 0
        return cogs

    # Fungsi untuk menghitung profit
    def calculate_profit(self):
        return self.price - self.calculate_cogs()

# ======================================================================
# PILAR 2: BUKU RESEP
# ======================================================================

class ProductRecipe(models.Model):
    """
    Model ini adalah "Buku Resep". Menghubungkan Produk Jadi dengan Bahan-Bahan
    yang dibutuhkan untuk membuatnya.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='recipes')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(verbose_name="Jumlah yang Dibutuhkan")

    def __str__(self):
        return f"Resep {self.product.name}: {self.quantity} {self.ingredient.unit} {self.ingredient.name}"

# ======================================================================
# PILAR 3: PENCATATAN PRODUKSI (BAHAN SETENGAH JADI)
# ======================================================================

class Production(models.Model):
    """
    Model ini untuk mencatat proses produksi bahan setengah jadi.
    Contoh: Membuat 1000ml Gula Cair dari 500gr Gula dan 500ml Air.
    """
    ingredient_produced = models.ForeignKey(Ingredient, on_delete=models.CASCADE, limit_choices_to={'type': 'BSJ'})
    quantity_produced = models.FloatField(verbose_name="Jumlah Dihasilkan")
    production_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Produksi {self.quantity_produced} {self.ingredient_produced.unit} {self.ingredient_produced.name}"

# ======================================================================
# MODEL-MODEL LAMA (dengan sedikit penyesuaian jika ada)
# ======================================================================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Kategori")
    def __str__(self):
        return self.name

class Transaction(models.Model):
    # ... (Model Transaction tidak berubah) ...
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Waktu Transaksi")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Harga")
    cash_received = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Uang Tunai", default=0)
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kembalian", default=0)

class TransactionDetail(models.Model):
    # ... (Model TransactionDetail tidak berubah) ...
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)