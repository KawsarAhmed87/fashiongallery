
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemAccountForm, ItemAccountUpdateForm
from .models import Item_account

from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#@login_required(login_url='login_user')
#@user_passes_test(lambda u: u.is_staff)
def create_item_account(request):
    if request.method == 'POST':
        form = ItemAccountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item account created successfully')
            return redirect('list_item_account')
        else:
            messages.error(request, 'Error creating item account. Please try again.')
    else:
        form = ItemAccountForm()
    
    context = {
        'form': form,
        'link': 'create_item_account'
    }
    
    return render(request, 'backend/item_account/create_item_account.html', context)

def edit_item_account(request, id):
    item_account = get_object_or_404(Item_account, id=id)
    if request.method == 'POST':
        form = ItemAccountUpdateForm(request.POST, request.FILES, instance=item_account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand updated successfully')
            return redirect('list_brand')
        else:
            messages.error(request, 'Error updating brand. Please try again.')
    else:
        form = ItemAccountUpdateForm(instance=item_account)
        
    context = {
        'item_account' : item_account,
        'form' : form
    }        
    return render(request, 'backend/item_account/edit_item_account.html', context)

def list_item_account(request):
    items_account = Item_account.objects.order_by('-id')
    
    paginator = Paginator(items_account, 10) 
    page_number = request.GET.get('page')
    paginated_items = paginator.get_page(page_number)
    
    context = {
        'items_account': paginated_items,
        'link': 'list_item_account'
    }

    return render(request, 'backend/item_account/list_item_account.html', context)

def delete_item_account(request,pk):
    data = get_object_or_404(Item_account, pk=pk)
    data.delete()
    messages.info(request, 'Item account deleted successfully.')
    return JsonResponse({'success': True})
