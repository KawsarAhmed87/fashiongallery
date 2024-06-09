
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, TagUpdateForm
from .models import Tag

from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator


#@login_required(login_url='login_user')
#@user_passes_test(lambda u: u.is_staff)
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'tag created successfully')
            return redirect('list_tag')
        else:
            messages.error(request, 'Error creating tag. Please try again.')
    else:
        form = TagForm()
    
    context = {
        'form': form,
        'link': 'create_tag'
    }
    return render(request, 'backend/tag/create_tag.html', context)

def edit_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    if request.method == 'POST':
        form = TagUpdateForm(request.POST, request.FILES, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'tag updated successfully')
            return redirect('list_tag')
        else:
            messages.error(request, 'Error updating tag. Please try again.')
    else:
        form = TagUpdateForm(instance=tag)
        
    context = {
        'tag' : tag,
        'form' : form
    }        
    return render(request, 'backend/tag/edit_tag.html', context)

def list_tag(request):
    tags = Tag.objects.order_by('-id')
    paginator = Paginator(tags, 10) 
    page = request.GET.get('page')
    tags = paginator.get_page(page)
    context = {
        'tags': tags,
        'link': 'list_tag'
    }

    return render(request, 'backend/tag/list_tag.html', context)

def delete_tag(request,pk):
    data = get_object_or_404(Tag, pk=pk)
    data.delete()
    messages.info(request, 'tag deleted successfully.')
    return JsonResponse({'success': True})
