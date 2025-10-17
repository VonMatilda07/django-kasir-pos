# kasir/admin.py

from django.contrib import admin
from .models import Category, Product, Ingredient, ProductRecipe, Production, Transaction, TransactionDetail

# 1. Buat inline untuk resep agar bisa diedit di halaman Produk
class ProductRecipeInline(admin.TabularInline):
    model = ProductRecipe
    extra = 1  # Jumlah form kosong yang ditampilkan

# 2. Buat custom admin untuk Produk
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    inlines = [ProductRecipeInline]

# 3. Daftarkan model-model lainnya seperti biasa
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Production)

# 4. Daftarkan juga model Transaksi biar bisa kita lihat datanya
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_price')
    readonly_fields = ('created_at',)

admin.site.register(TransactionDetail)