from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from product.models import Product, Comment
from category.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Avg

# Create your views here.
def home(request):
    products = Product.objects.order_by('-id')[:6]
    featured_categories = Category.objects.filter(featured=True,category_product__isnull=False
    ).distinct().order_by('?')[:6]
    featured_products = Product.objects.filter(featured=True).order_by('-created_date')[:6]
    context = {
        'products' : products,
        'featured_categories' : featured_categories,
        'featured_products': featured_products
    }
    return render(request, 'frontend/pages/index.html', context)
def all_products(request):
    products = Product.objects.order_by('-id')
    
    paginator = Paginator(products, 12)  # Display 10 products per page
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    context = {
        'products' : products_page
    }
    
    return render(request, 'frontend/pages/all_products.html', context)

def generate_star_rating_html(rating):
    if rating is None:
        rating = 0
    full_stars = int(rating)
    half_star = rating - full_stars >= 0.5
    empty_stars = 5 - full_stars - half_star

    star_html = "".join('<small class="fas fa-star"></small>' for _ in range(full_stars))
    if half_star:
        star_html += '<small class="fas fa-star-half-alt"></small>'
    star_html += "".join('<small class="far fa-star"></small>' for _ in range(empty_stars))
    
    return star_html

def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    average_rating = Comment.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    average_rating_scaled = round(average_rating * 5 / 5.0, 1) if average_rating else 0
    rating_html = generate_star_rating_html(average_rating_scaled)
    
    context = {
        'product': product,
        'generate_star_rating_html': rating_html
    }
    return render(request, 'frontend/pages/product_details.html', context)

def category_products(request, slug):
    # Retrieve the category based on the category_slug
    category = get_object_or_404(Category, slug=slug)

    # Retrieve all products belonging to the specified category
    products = Product.objects.filter(category=category)

    # Pass the category and its products to the template
    return render(request, 'frontend/pages/category_products.html', {'category': category, 'products': products})


def search_products(query):
    # Use Q objects to create the search conditions
    search_conditions = Q(name__icontains=query) | \
                        Q(sku__icontains=query) | \
                        Q(slug__icontains=query) | \
                        Q(category__name__icontains=query) | \
                        Q(tags__name__icontains=query) | \
                        Q(brand__name__icontains=query) | \
                        Q(sizes__name__icontains=query) | \
                        Q(colours__name__icontains=query) | \
                        Q(price__icontains=query) | \
                        Q(info__icontains=query) | \
                        Q(description__icontains=query)

    # Perform the search query
    search_results = Product.objects.filter(search_conditions).distinct()

    return search_results

def product_search(request):
    template_name = 'frontend/pages/search_products.html'
    query = request.GET.get('search') 
    search_results = []

    if not query:
        # Query is empty, redirect back to the search form
        return redirect('home')
    
    search_results = search_products(query)

    context = {
        'query': query,
        'search_results': search_results,
    }
    return render(request, template_name, context)

def dashboard(request):
    year = timezone.localtime(timezone.now()).strftime('%Y')
    context = {
        'year' : year,
        'link' : "dashboard"
    }
    return render(request, 'backend/dashboard/index.html', context)
