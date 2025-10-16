# kasir/urls.py

from django.urls import path
# Tambahkan sales_report_view
from .views import cashier_view, process_transaction_view, transaction_receipt_view, sales_report_view

urlpatterns = [
    path('', cashier_view, name='cashier_page'),
    path('process-transaction/', process_transaction_view, name='process_transaction'),
    path('receipt/<int:transaction_id>/', transaction_receipt_view, name='transaction_receipt'),
    # URL baru untuk laporan
    path('report/', sales_report_view, name='sales_report'),
]