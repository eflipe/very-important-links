from vil_app.models import Category, Page
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


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


class CategoryCreate(CreateView):
    model = Category
    fields = ('name', )
    success_url = reverse_lazy('index')


class PageCreate(CreateView):
    model = Page
    fields = ('title', 'name')
    success_url = reverse_lazy('index')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data
