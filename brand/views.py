
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BrandForm, BrandUpdateForm
from .models import Brand

from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#@login_required(login_url='login_user')
#@user_passes_test(lambda u: u.is_staff)
def create_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand created successfully')
            return redirect('list_brand')
        else:
            messages.error(request, 'Error creating brand. Please try again.')
    else:
        form = BrandForm()
    
    context = {
        'form': form,
        'link': 'create_brand'
    }
    
    return render(request, 'backend/brand/create_brand.html', context)

def edit_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    if request.method == 'POST':
        form = BrandUpdateForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand updated successfully')
            return redirect('list_brand')
        else:
            messages.error(request, 'Error updating brand. Please try again.')
    else:
        form = BrandUpdateForm(instance=brand)
        
    context = {
        'brand' : brand,
        'form' : form
    }        
    return render(request, 'backend/brand/edit_brand.html', context)

def list_brand(request):
    brands = Brand.objects.order_by('-id')
    paginator = Paginator(brands, 10) 
    page = request.GET.get('page')
    brands = paginator.get_page(page)
    context = {
        'brands': brands,
        'link': 'list_brand'
    }

    return render(request, 'backend/brand/list_brand.html', context)

def delete_brand(request,pk):
    data = get_object_or_404(Brand, pk=pk)
    data.delete()
    messages.info(request, 'Brand deleted successfully.')
    return JsonResponse({'success': True})
