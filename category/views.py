
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm, CategoryUpdateForm
from .models import Category

from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator



def delete_category(request,pk):
    data = get_object_or_404(Category, pk=pk)
    data.delete()
    messages.info(request, 'Category deleted successfully.')
    return JsonResponse({'success': True})

#@login_required(login_url='login_user')
#@user_passes_test(lambda u: u.is_staff)
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully')
            return redirect('list_category')
        else:
            messages.error(request, 'Error creating category. Please try again.')
    else:
        form = CategoryForm()
    
    context = {
        'link' : 'create_category',
        'form' : form,
    } 
        
    return render(request, 'backend/category/create_category.html', context)

def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryUpdateForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('list_category')
        else:
            messages.error(request, 'Error updating category. Please try again.')
    else:
        form = CategoryUpdateForm(instance=category)
        
    context = {
        'category' : category,
        'form' : form,
    }        
    return render(request, 'backend/category/edit_category.html', context)

def list_category(request):
    categories = Category.objects.order_by('-id')
    paginator = Paginator(categories, 10) 
    page = request.GET.get('page')
    categories = paginator.get_page(page)
    context = {
        'categories': categories,
        'link' : 'list_category'
    }


    return render(request, 'backend/category/list_category.html', context)
