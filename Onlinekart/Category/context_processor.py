from .models import *


def category(request):
    categories = Category.objects.all()
    return dict(categories=categories)
