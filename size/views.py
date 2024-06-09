
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SizeForm, SizeUpdateForm
from .models import Size

from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator


#@login_required(login_url='login_user')
#@user_passes_test(lambda u: u.is_staff)
def create_size(request):
    if request.method == 'POST':
        form = SizeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'size created successfully')
            return redirect('list_size')
        else:
            messages.error(request, 'Error creating size. Please try again.')
    else:
        form = SizeForm()
    
    context = {
        'form': form,
        'link': 'create_size'
    }
        
    return render(request, 'backend/size/create_size.html', context)

def edit_size(request, id):
    size = get_object_or_404(Size, id=id)
    if request.method == 'POST':
        form = SizeUpdateForm(request.POST, request.FILES, instance=size)
        if form.is_valid():
            form.save()
            messages.success(request, 'size updated successfully')
            return redirect('list_size')
        else:
            messages.error(request, 'Error updating size. Please try again.')
    else:
        form = SizeUpdateForm(instance=size)
        
    context = {
        'size' : size,
        'form' : form
    }        
    return render(request, 'backend/size/edit_size.html', context)

def list_size(request):
    sizes = Size.objects.order_by('-id')
    paginator = Paginator(sizes, 10) 
    page = request.GET.get('page')
    sizes = paginator.get_page(page)
    context = {
        'sizes': sizes,
        'link': 'list_size'
    }

    return render(request, 'backend/size/list_size.html', context)

def delete_size(request,pk):
    data = get_object_or_404(Size, pk=pk)
    data.delete()
    messages.info(request, 'size deleted successfully.')
    return JsonResponse({'success': True})
