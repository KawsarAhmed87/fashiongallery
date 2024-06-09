from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from stock.models import Stock
from order.forms import OrderForm
from user.models import User
from order.models import Order
from django.http import JsonResponse
from accounts.models import Accounts
from item_account.models import Item_account 
from django.contrib import messages
from django.utils import timezone
from order.models import Coupon
import random
import string

def generate_order_no():
    letters = string.ascii_uppercase
    digits = string.digits
    order_no = ''.join(random.choice(letters + digits) for i in range(12))
    return order_no


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        size = request.POST.get('size')
        colour = request.POST.get('colour')
        
        if not size or not colour:
            previous_url = request.META.get('HTTP_REFERER', '/')
            messages.error(request, 'Please select a size and colour')
            return redirect(previous_url)

        price = float(product.discount_price) if product.discount_price else float(product.price)
        
        cart = request.session.get('cart', [])
        found = False

        for item in cart:
            if item['id'] == product_id and item['info'] == f"size: {size}, colour: {colour}":
                item['quantity'] += 1
                found = True
                break

        if not found:
            cart.append({
                'id': product_id,
                'image': product.image.url,
                'name': product.name,
                'info': f'size: {size}, colour: {colour}',
                'price': price,
                'quantity': 1
            })

        request.session['cart'] = cart
        update_cart_data(request)
        previous_url = request.META.get('HTTP_REFERER', '/')
        return redirect(previous_url)

    return redirect('home')

def cart(request):
    current_date = timezone.now().date()
    cart = request.session.get('cart', {})
    request.session['cart_data'] = {'shipping': 0, 'net_total': 0, 'product_number': 0, 'discount': 0}
   
    discount = 0  
    
        
    for item in cart:
        item['subtotal'] = item['price'] * item['quantity']
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    if request.method == "POST":
        coupon_no = request.POST.get('coupon')
        coupon = Coupon.objects.filter(coupon_no=coupon_no).first()

        if coupon:
            if coupon.start_date <= current_date and coupon.end_date >= current_date and coupon.min_shop_amount <= total:
                discount = coupon.coupon_amount
                messages.success(request, 'Coupon discount has been applied successfully')
            else:
                discount = 0
                messages.error(request, 'Coupon discount has not been applied')
        else:
            if coupon_no is not None:
                messages.error(request, 'Your coupon is incorrect')
            
    if cart:
        shipping = 20.0   
        cart_data = {'total': total, 'shipping': shipping, 'discount': int(discount), 'net_total': total+shipping-float(discount), 'product_number': len(cart)}
        request.session['cart_data'] = cart_data

    context = {
        'cart': cart,
         'total': total
         }
    return render(request, 'frontend/pages/cart/cart.html', context)


def checkout(request):
    cart = request.session.get('cart', {})
    cart_data = request.session.get('cart_data', {})
    
    for item in cart:
        item['subtotal'] = item['price'] * item['quantity']
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        form = OrderForm(request.POST)
        
        if form.is_valid():
            order = form.save(commit=False)
            order.order_no = 'S-' + generate_order_no()  # Using the generate_order_no function
            order.customer = user
            order.address = form.cleaned_data.get('address')
            order.total = cart_data['total']
            order.shipping = cart_data['shipping']
            order.save()
            
            # Fetching cash and sales accounts based on slug
            cash_account = get_object_or_404(Item_account, slug='cash')
            sales_account = get_object_or_404(Item_account, slug='sale')
            
            # Create accounting entry for the order
            Accounts.objects.create(
                date=order.order_date,
                order_info=order,
                debit=cash_account,
                credit=sales_account,
                amount=order.total,
                created_by=user
            )
            
            for item in cart:
                product = get_object_or_404(Product, id=item['id'])
                Stock.objects.create(
                    order=order,
                    date=order.order_date,
                    product=product,
                    quantity_out=item['quantity'],
                    price=item['price']
                )
                product.reduce_quantity(item['quantity'])
            
            # Clear the cart after successful checkout
            request.session.pop('cart')
            request.session.pop('cart_data')
            
            return redirect('home')
    else:
        form = OrderForm()
    
    context = {
        'cart': cart,
        'cart_data': cart_data,
        'total': total,
        'form': form
    }
    return render(request, 'frontend/pages/cart/checkout.html', context)

def update_cart_data(request):
    cart = request.session.get('cart', [])
    total_items = len(cart)  # Count of distinct items
    total_quantity = sum(item['quantity'] for item in cart)
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    shipping = 20.0 if cart else 0.0
    discount = request.session.get('cart_data', {}).get('discount', 0)
    
    cart_data = {
        'total': total_price,
        'shipping': shipping,
        'discount': discount,
        'net_total': total_price + shipping - discount,
        'product_number': total_items,  # Number of distinct items
        'total_quantity': total_quantity  # Total quantity of all items
    }
    request.session['cart_data'] = cart_data


def update_cart(request, index):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        action = request.POST.get('action')
        
        if 0 <= index < len(cart):
            if action == 'add':
                cart[index]['quantity'] += 1
            elif action == 'subtract' and cart[index]['quantity'] > 1:
                cart[index]['quantity'] -= 1

        request.session['cart'] = cart
        update_cart_data(request)  # Ensure cart data is updated
        return redirect('cart')

    return redirect('cart')



def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    if 0 <= index < len(cart):
        del cart[index]
        request.session['cart'] = cart
        update_cart_data(request)  # Ensure cart data is updated
    return redirect('cart')



def clear_cart(request):
    request.session.pop('cart', None)
    request.session.pop('cart_data', None)
    return redirect('cart')

def list_order(request):
    orders = Order.objects.order_by('-id')
            
    context = {
        'orders': orders
    }
    return render(request, 'backend/order/list_order.html', context)

def view_order(request, id):
    order = get_object_or_404(Order, id=id)
    stocks = order.order_stock.all()  # Retrieve all associated stocks for the purchase
    context = {
        'order': order,
        'stocks': stocks
    }
    return render(request, 'backend/order/view_order.html', context)

def delete_order(request, pk):
    data = get_object_or_404(Order, pk=pk)
    data.delete()
    messages.info(request, 'Order deleted successfully.')
    return JsonResponse({'success': True})



import os 
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.conf import settings
from .models import Product
from io import BytesIO



def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = [os.path.realpath(path) for path in result]
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path


def render_pdf_download(request, id):
    template_path = 'backend/order/products_template.html'
    
    # Retrieve the products list from the database
    order = get_object_or_404(Order, id=id)
    stocks = order.order_stock.all()  # Retrieve all associated stocks for the purchase
    
    # Pass the products list to the template context
    context = {'order': order, 'stocks': stocks}

    # Create a Django response object with content_type set to pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'

    # Render the template to HTML
    html = render_to_string(template_path, context)

    # Create a PDF
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    # If there are any errors, return a response with error details
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response










