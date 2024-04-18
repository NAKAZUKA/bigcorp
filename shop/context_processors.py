from .models import Category


def categories(request):
    """функция для получения списка категорий"""
    return {'categories': Category.objects.filter(parent=None)}
