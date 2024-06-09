from .models import Category

def category_context(request):
    # Retrieve all categories (or apply any specific filtering you need)
    get_categories = Category.objects.all()
    return {'get_categories': get_categories}