# kasir/urls.py

from django.urls import path
from .views import (
    cashier_view, 
    process_transaction_view, 
    transaction_receipt_view, 
    sales_report_view,
    dashboard_view,
    sales_data_api, # <-- PERUBAHAN: Nama view API diperbarui
    top_products_api
)

urlpatterns = [
    # Halaman Utama
    path('', cashier_view, name='cashier_page'),
    path('receipt/<int:transaction_id>/', transaction_receipt_view, name='transaction_receipt'),
    path('report/', sales_report_view, name='sales_report'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # API Endpoints (untuk data)
    path('process-transaction/', process_transaction_view, name='process_transaction'),
    # VVV PERUBAHAN: URL dan nama API diperbarui VVV
    path('api/sales-data/', sales_data_api, name='sales_data_api'),
    path('api/top-products/', top_products_api, name='top_products_api'),
]