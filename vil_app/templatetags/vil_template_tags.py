from django import template
from vil_app.models import Category # CategoryListView: clave para después comprender el {% get_category_list categorias %} 

register = template.Library()


@register.inclusion_tag('vil_app/categorias_tag.html')
def get_category_list(current_category=None):
    return {'categorias': Category.objects.all(),
            'current_category': current_category}
