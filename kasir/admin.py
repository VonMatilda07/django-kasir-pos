# kasir/admin.py

from django.contrib import admin
from .models import Category, Product

# Daftarkan model Category dan Product di sini
admin.site.register(Category)
admin.site.register(Product)