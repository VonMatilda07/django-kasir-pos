# kasir/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from .models import Product, Transaction, TransactionDetail
import json
from django.utils import timezone
from datetime import timedelta, datetime # <-- PERUBAHAN: Tambahkan 'datetime'
from django.db.models import Sum, Count
from django.db.models.functions import TruncHour

# ===================================================================
# View-view standar (tidak ada perubahan di sini)
# ===================================================================

@login_required
def cashier_view(request):
    products = Product.objects.all()
    products_list = list(products.values('id', 'name', 'price','stock'))
    context = {'products': products, 'products_json': products_list}
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
                    transaction=transaction, product=product,
                    quantity=item['quantity'], subtotal=item['price'] * item['quantity']
                )
                product.stock -= item['quantity']
                product.save()
            return JsonResponse({'status': 'success', 'message': 'Transaksi berhasil disimpan!', 'transaction_id': transaction.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def transaction_receipt_view(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    context = {'transaction': transaction}
    return render(request, 'kasir/receipt.html', context)

@permission_required('kasir.view_transaction', raise_exception=True)
def sales_report_view(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    context = {'transactions': transactions}
    return render(request, 'kasir/report.html', context)

# ===================================================================
# View-view untuk Dashboard (SEMUA SUDAH DIPERBARUI)
# ===================================================================

@permission_required('kasir.view_transaction', raise_exception=True)
def dashboard_view(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = timezone.now().date()

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = start_date

    transactions_in_range = Transaction.objects.filter(created_at__date__range=[start_date, end_date])

    total_sales = transactions_in_range.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_transactions = transactions_in_range.count()
    average_per_transaction = total_sales / total_transactions if total_transactions > 0 else 0
    
    context = {
        'total_sales_today': total_sales,
        'total_transactions_today': total_transactions,
        'average_per_transaction': average_per_transaction,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    return render(request, 'kasir/dashboard.html', context)


@permission_required('kasir.view_transaction', raise_exception=True)
def sales_data_api(request): # <-- Nama fungsi diubah
    start_date_str = request.GET.get('start_date', timezone.now().strftime('%Y-%m-%d'))
    end_date_str = request.GET.get('end_date', start_date_str)

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Hitung durasi filter dalam hari
    duration = (end_date - start_date).days + 1 

    labels = []
    data_sales = []

    if duration == 1: # Jika rentang hanya 1 hari, tampilkan per jam
        transactions = Transaction.objects.filter(created_at__date=start_date)
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
        data_sales = hourly_sales_data
        title = f"Penjualan per Jam ({start_date.strftime('%d %b %Y')})"

    else: # Jika rentang lebih dari 1 hari, tampilkan per hari
        transactions = Transaction.objects.filter(created_at__date__range=[start_date, end_date])
        sales_by_day = transactions.annotate(
            day=TruncHour('created_at') # TruncHour works for day if no time specified, but we can use __date
        ).values('day').annotate(
            total_sales=Sum('total_price')
        ).order_by('day')

        # Kita perlu membuat daftar semua tanggal dalam rentang untuk memastikan semua label ada
        current_date = start_date
        sales_map = {entry['day'].date(): float(entry['total_sales']) for entry in sales_by_day}

        while current_date <= end_date:
            labels.append(current_date.strftime('%d %b')) # Format tanggal untuk label
            data_sales.append(sales_map.get(current_date, 0)) # Ambil data atau 0 jika tidak ada transaksi
            current_date += timedelta(days=1)

        title = f"Penjualan per Hari ({start_date.strftime('%d %b')} - {end_date.strftime('%d %b %Y')})"

    data = {
        'labels': labels,
        'data': data_sales,
        'title': title, # <-- Tambahkan title untuk dynamic display
        'type': 'bar' # <-- Tambahkan type jika suatu hari ingin ganti jenis grafik
    }
    return JsonResponse(data)

@permission_required('kasir.view_transaction', raise_exception=True)
def top_products_api(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else start_date
    else:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

    product_sales = TransactionDetail.objects.filter(
        transaction__created_at__date__range=[start_date, end_date]
    ).values('product__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')

    top_5_products = list(product_sales[:5])
    bottom_5_products = list(product_sales.order_by('total_sold')[:5])
    data = {'top_products': top_5_products, 'bottom_products': bottom_5_products}
    return JsonResponse(data)