from vil_app.models import Category, Page
from django.views import generic


class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'categorias'
    queryset = Category.objects.order_by('-likes')[:5]
    template_name = 'vil_app/index.html'

# entrar por el Category model???


class ShowpagesDetailView(generic.DetailView):
    model = Category
    # queryset = Category.objects.get(slug=pk)
    context_object_name = 'categorias'
    template_name = 'vil_app/show_pages.html'
