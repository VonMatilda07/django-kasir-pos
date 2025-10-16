# kasir/views.py

from django.shortcuts import render
from django.http import JsonResponse
# 1. Import 'login_required'
from django.contrib.auth.decorators import permission_required, login_required
from .models import Product, Transaction, TransactionDetail
import json

@login_required # <-- TAMBAHKAN INI
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
            cash_received = data.get('cash_received') # <-- 1. Ambil data uang tunai dari JS

            # 2. Hitung kembalian
            change = float(cash_received) - float(total)

            # 3. Simpan semua data ke database
            transaction = Transaction.objects.create(
                total_price=total,
                cash_received=cash_received,
                change_amount=change
            )

            # Loop 'for' untuk menyimpan detail transaksi (tidak ada perubahan di sini)
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

            # return JsonResponse (tidak ada perubahan di sini)
            return JsonResponse({
                'status': 'success', 
                'message': 'Transaksi berhasil disimpan!',
                'transaction_id': transaction.id
            })
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required # <-- TAMBAHKAN INI
def transaction_receipt_view(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    context = {
        'transaction': transaction
    }
    return render(request, 'kasir/receipt.html', context)


@login_required # <-- TAMBAHKAN INI
@permission_required('kasir.view_transaction', raise_exception=True)
def sales_report_view(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    context = {
        'transactions': transactions
    }
    return render(request, 'kasir/report.html', context)