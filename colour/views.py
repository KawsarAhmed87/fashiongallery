
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ColourForm, ColourUpdateForm
from .models import Colour

from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#@login_required(login_url='login_user')
#@user_passes_test(lambda u: u.is_staff)
def create_colour(request):
    if request.method == 'POST':
        form = ColourForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'colour created successfully')
            return redirect('list_colour')
        else:
            messages.error(request, 'Error creating colour. Please try again.')
    else:
        form = ColourForm()
    
    context = {
        'form': form,
        'link': 'create_colour'
    }
        
    return render(request, 'backend/colour/create_colour.html', context)

def edit_colour(request, id):
    colour = get_object_or_404(Colour, id=id)
    if request.method == 'POST':
        form = ColourUpdateForm(request.POST, request.FILES, instance=colour)
        if form.is_valid():
            form.save()
            messages.success(request, 'colour updated successfully')
            return redirect('list_colour')
        else:
            messages.error(request, 'Error updating colour. Please try again.')
    else:
        form = ColourUpdateForm(instance=colour)
        
    context = {
        'colour' : colour,
        'form' : form
    }        
    return render(request, 'backend/colour/edit_colour.html', context)

def list_colour(request):
    colours = Colour.objects.order_by('-id')
    paginator = Paginator(colours, 10) 
    page = request.GET.get('page')
    colours = paginator.get_page(page)
    context = {
        'colours': colours,
        'link': 'list_colour'
    }

    return render(request, 'backend/colour/list_colour.html', context)

def delete_colour(request,pk):
    data = get_object_or_404(Colour, pk=pk)
    data.delete()
    messages.info(request, 'colour deleted successfully.')
    return JsonResponse({'success': True})
