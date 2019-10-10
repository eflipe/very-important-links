from vil_app.models import Category, Page, UserProfile
from django import forms
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


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
    fields = ('title', 'url')
    # success_url = reverse_lazy('index')
    def form_valid(self, form):

        page = form.save(commit=False)

        page.category = get_object_or_404(Category,

                                          slug=self.kwargs.get('slug'))

        return super(PageCreate, self).form_valid(form)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

    def get_success_url(self):
        return reverse_lazy('vil_app:categoria', kwargs={'slug': self.kwargs['slug']})


class UserCreate(CreateView):
    model = User
    fields = ('username', 'email', 'password')
    template_name = 'registracion/registracion.html'
    success_url = reverse_lazy('index')
    password = forms.CharField(widget=forms.PasswordInput())
