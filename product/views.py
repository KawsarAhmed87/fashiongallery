from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, CommentForm, ReplyForm
from category.models import Category
from tag.models import Tag
from brand.models import Brand
from size.models import Size
from colour.models import Colour
from .models import Product, Comment, Reply
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
import os


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.image:
        if os.path.isfile(product.image.path):
            os.remove(product.image.path)
    
    product.delete()
    messages.info(request, 'Product deleted successfully.')
    return JsonResponse({'success': True})


def create_product(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    brands = Brand.objects.all()
    sizes = Size.objects.all()
    colours = Colour.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            
            tags = form.cleaned_data['tags']
            product.tags.set(tags)
               
            sizes = form.cleaned_data['sizes']
            product.sizes.set(sizes)
            
            colours = form.cleaned_data['colours']
            product.colours.set(colours)
                
            messages.success(request, 'Product created successfully')
            return redirect('list_product')
        else:
            messages.error(request, 'Error creating product. Please try again.')
    else:
        form = ProductForm()
    context = {
        'categories' : categories,
        'tags' : tags,
        'brands' : brands,
        'sizes' : sizes,
        'colours' : colours,
        'form'  : form
    }
    return render(request, 'backend/product/create_product.html', context)
def list_product(request):
    products = Product.objects.order_by('-id')
    paginator = Paginator(products, 10) 
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {
        'products' : products
    }
    return render(request, 'backend/product/list_product.html', context)

def view_product(request, id, slug):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    brands = Brand.objects.all()
    sizes = Size.objects.all()
    colours = Colour.objects.all()
    
    product = get_object_or_404(Product, id=id)

    context = {
        'categories' : categories,
        'tags' : tags,
        'brands' : brands,
        'sizes' : sizes,
        'colours' : colours,
        'product' : product
    }
    return render(request, 'backend/product/view_product.html', context)

def edit_product(request, id, slug):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    brands = Brand.objects.all()
    sizes = Size.objects.all()
    colours = Colour.objects.all()
    
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            
            tags = form.cleaned_data['tags']
            product.tags.set(tags)
               
            sizes = form.cleaned_data['sizes']
            product.sizes.set(sizes)
            
            colours = form.cleaned_data['colours']
            product.colours.set(colours)
            messages.success(request, 'Product updated successfully')
            return redirect('list_product')
    else:
        form = ProductForm(instance=product)
    context = {
        'categories' : categories,
        'tags' : tags,
        'brands' : brands,
        'sizes' : sizes,
        'colours' : colours,
        'form'  : form,
        'product' : product
    }
    return render(request, 'backend/product/edit_product.html', context)


def comment_review(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            rating = int(form.cleaned_data['rating'])
            text = form.cleaned_data['text']
            
            # Create and save the comment using the model's manager
            Comment.objects.create(
                product=product,
                rating=rating,
                text=text,
                user=request.user
            )
            messages.success(request, 'Comment added successfully.')
            # Redirect to the product_details view with the product's slug parameter
            return redirect('product_details', slug=product.slug)
        else:
            messages.error(request, 'Comment not added.')
    else:
        messages.info(request, 'Somethings went wrong.')

    return redirect('product_details', slug=product.slug)



def reply_comment(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            comment_id = form.cleaned_data['comment_id']
            comment = get_object_or_404(Comment, pk=comment_id)
            text = form.cleaned_data['text']
            
            # Create and save the reply using the model's manager
            Reply.objects.create(
                user=request.user,
                comment=comment,
                text=text
            )
            messages.success(request, 'Reply added successfully.')
            # Redirect to the product_details view with the product's slug parameter
            return redirect('product_details', slug=product.slug)
        else:
            messages.error(request, 'Reply not added.')
    else:
        messages.info(request, 'Somethings went wrong.')

    return redirect('product_details', slug=product.slug)
