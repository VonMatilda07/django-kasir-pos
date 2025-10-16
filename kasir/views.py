# kasir/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from .models import Product, Transaction, TransactionDetail
import json
from django.utils import timezone
from django.db.models import Sum, Count # <-- PERUBAHAN: Tambahkan 'Count'
from django.db.models.functions import TruncHour
from datetime import timedelta # Tambahkan ini di import timezone

@login_required
def cashier_view(request):
    products = Product.objects.all()
    products_list = list(products.values('id', 'name', 'price'))
    
    context = {
        'products': products,
        'products_json': products_list, 
    }
    return render(request, 'kasir/cashier.html', context)


def process_transaction_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_data = data.get('cart')
            total = data.get('total')
            cash_received = data.get('cash_received')

            change = float(cash_received) - float(total)

            transaction = Transaction.objects.create(
                total_price=total,
                cash_received=cash_received,
                change_amount=change
            )

            for product_id, item in cart_data.items():
                product = Product.objects.get(id=product_id)
                TransactionDetail.objects.create(
                    transaction=transaction,
                    product=product,
                    quantity=item['quantity'],
                    subtotal=item['price'] * item['quantity']
                )
                product.stock -= item['quantity']
                product.save()

            return JsonResponse({
                'status': 'success', 
                'message': 'Transaksi berhasil disimpan!',
                'transaction_id': transaction.id
            })
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def transaction_receipt_view(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    context = {
        'transaction': transaction
    }
    return render(request, 'kasir/receipt.html', context)


@permission_required('kasir.view_transaction', raise_exception=True)
def sales_report_view(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    context = {
        'transactions': transactions
    }
    return render(request, 'kasir/report.html', context)

# --- FUNGSI INI SUDAH DIPERBARUI ---
@permission_required('kasir.view_transaction', raise_exception=True)
def dashboard_view(request):
    # 1. Ambil data transaksi hanya untuk hari ini
    today = timezone.now().date()
    transactions_today = Transaction.objects.filter(created_at__date=today)

    # 2. Hitung KPI
    total_sales_today = transactions_today.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_transactions_today = transactions_today.count()

    # 3. Hitung rata-rata, hindari pembagian dengan nol
    average_per_transaction = 0
    if total_transactions_today > 0:
        average_per_transaction = total_sales_today / total_transactions_today
    
    # 4. Kirim data KPI ke template
    context = {
        'total_sales_today': total_sales_today,
        'total_transactions_today': total_transactions_today,
        'average_per_transaction': average_per_transaction,
    }
    return render(request, 'kasir/dashboard.html', context)


@permission_required('kasir.view_transaction', raise_exception=True)
def sales_per_hour_api(request):
    today = timezone.now().date()
    transactions = Transaction.objects.filter(created_at__date=today)

    sales_by_hour = transactions.annotate(
        hour=TruncHour('created_at')
    ).values('hour').annotate(
        total_sales=Sum('total_price')
    ).order_by('hour')

    hourly_sales_data = [0] * 24
    for entry in sales_by_hour:
        hour_index = entry['hour'].hour
        hourly_sales_data[hour_index] = float(entry['total_sales'])

    labels = [f"{h:02d}:00" for h in range(24)]

    data = {
        'labels': labels,
        'data': hourly_sales_data,
    }
    return JsonResponse(data)

@permission_required('kasir.view_transaction', raise_exception=True)
def top_products_api(request):
    # 1. Tentukan rentang waktu (30 hari terakhir)
    start_date = timezone.now() - timedelta(days=30)

    # 2. Hitung jumlah penjualan per produk
    product_sales = TransactionDetail.objects.filter(
        transaction__created_at__gte=start_date
    ).values('product__name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold') # Urutkan dari yang paling banyak terjual

    # 3. Ambil 5 produk terlaris dan 5 produk paling tidak laku
    top_5_products = list(product_sales[:5])
    bottom_5_products = list(product_sales.order_by('total_sold')[:5])

    data = {
        'top_products': top_5_products,
        'bottom_products': bottom_5_products,
    }
    return JsonResponse(data)