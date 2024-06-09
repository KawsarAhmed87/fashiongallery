
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from purchase.models import Supplier, Purchase
from stock.models import Stock
from django.contrib import messages
from purchase.forms import PurchaseForm
from django.db import transaction
from item_account.models import Item_account
from accounts.models import Accounts  # Import the Accounts model
import random, string
from django.http import JsonResponse
from django.core.paginator import Paginator

def generate_purchase_no():
    letters_digits = string.ascii_uppercase + string.digits
    return 'P-' + ''.join(random.choice(letters_digits) for _ in range(10))


#@login_required(login_url='login_user')
#@user_passes_test(lambda u: u.is_staff)

    
def create_purchase(request):
    products = Product.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                purchase = form.save(commit=False)
                purchase.created_by = request.user
                purchase.purchase_no = generate_purchase_no()
                purchase.save()
                
                product_ids = request.POST.getlist('product_id[]')
                prices = request.POST.getlist('purchase_price[]')
                quantities = request.POST.getlist('purchase_quantity[]')
                
                total_amount = 0

                for product_id, quantity, price in zip(product_ids, quantities, prices):
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantity)
                    price = float(price)
                    total_amount += quantity * price
                    
                    product.increase_quantity(quantity)

                    if price != product.purchase_price:
                        product.purchase_price = price
                        product.save()

                    Stock.objects.create(
                        date=purchase.purchase_date,
                        purchase=purchase,
                        product=product,
                        quantity_in=quantity,
                        price=price
                    )

                purchase.total = total_amount
                purchase.save()

                # Fetch the debit account where slug is "purchase"
                debit_account = Item_account.objects.filter(slug='purchase').first()
                
                # Get the selected paid_by option from the form and fetch the corresponding item account
                paid_by = request.POST.get('paid_by')
                credit_account = Item_account.objects.filter(slug=paid_by).first()

                if not debit_account or not credit_account:
                    messages.error(request, 'Account information is incorrect.')
                    return redirect('create_purchase')

                # Create an Accounts entry with the fetched debit and credit accounts
                Accounts.objects.create(
                    date=purchase.purchase_date,
                    purchase_info=purchase,
                    order_info=None,  # Assuming no order info in this context
                    debit=debit_account,
                    credit=credit_account,
                    amount=total_amount,
                    created_by=request.user
                )

            messages.success(request, 'Purchase created successfully')
            return redirect('create_purchase')
        else:
            messages.error(request, 'Form submission failed. Please check the data entered.')
    else:
        form = PurchaseForm()

    context = {
        'products': products,
        'purchase_no': generate_purchase_no(),
        'suppliers': suppliers,
        'form': form
    }
    return render(request, 'backend/purchase/create_purchase.html', context)

def list_purchase(request):
    # Fetch all purchases ordered by the purchase date in descending order
    purchases = Purchase.objects.all().order_by('-purchase_date')
    # Paginator to paginate the purchases, showing 10 purchases per page
    paginator = Paginator(purchases, 10)  # Show 10 purchases per page

    # Get the current page number from the GET request
    page_number = request.GET.get('page')
    # Get the corresponding page object
    page_obj = paginator.get_page(page_number)

    context = {
        'purchases': page_obj  # Pass the page object to the template
    }
    return render(request, 'backend/purchase/list_purchase.html', context)
def view_purchase(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    account = purchase.purchase.first()
    stocks = purchase.purchase_stock.all()  # Retrieve all associated stocks for the purchase
    total_price = sum(item.quantity_in * item.price for item in stocks)
    context = {
        'purchase': purchase,
        'account': account,
        'stocks': stocks,
        'total_price': total_price,
    }
    return render(request, 'backend/purchase/view_purchase.html', context)


def delete_purchase(request, pk):
    data = get_object_or_404(Purchase, pk=pk)
    data.delete()
    messages.info(request, 'Purchase deleted successfully.')
    return JsonResponse({'success': True})
    