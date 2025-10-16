# kasir/urls.py

from django.urls import path
from .views import (
    cashier_view, 
    process_transaction_view, 
    transaction_receipt_view, 
    sales_report_view,
    dashboard_view,
    sales_per_hour_api,
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
    path('api/sales-per-hour/', sales_per_hour_api, name='sales_per_hour_api'),
    path('api/top-products/', top_products_api, name='top_products_api'),
]