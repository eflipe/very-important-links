from vil_app.models import Category, Page, UserProfile
from vil_app.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from yandex_search.yandex_search_1 import run_query

# def index(request):
#     categorias = Category.objects.order_by('-likes')[:3]  # subset
#     paginas = Page.objects.order_by('-fecha_agregado')
#     # frase = FrasesRandom.objects.all()
#     context_dict = {}
#     # frase_r = random.choice(frase)
#     # context_dict['frase'] = frase_r  # template context
#     context_dict['categorias'] = categorias  # 'categoris' es la key del dict
#     context_dict['paginas'] = paginas
#
#     template = 'vil_app/index.html'
#     response = render(request, template, context_dict)
#
#     return response


# buscador
def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # buscador
            result_list = run_query(query)
    return render(request, 'vil_app/search.html', {'result_list': result_list})


class PageListView(generic.ListView):
    model = Page
    context_object_name = 'paginas'
    queryset = Page.objects.order_by('-fecha_agregado')
    template_name = 'vil_app/index.html'


class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'categorias'
    queryset = Category.objects.order_by('-likes')[:5]
    template_name = 'vil_app/categorias_tag.html'

# entrar por el Category model???


class ShowpagesDetailView(generic.DetailView):
    model = Category
    # queryset = Category.objects.get(slug=pk)
    context_object_name = 'categorias'
    template_name = 'vil_app/show_pages.html'


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ('name', )
    success_url = reverse_lazy('index')


class PageCreate(LoginRequiredMixin, CreateView):
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
    form_class = UserCreationForm
    template_name = 'registration/registracion.html'
    success_url = reverse_lazy('index') # prox: al user profile

    def form_valid(self, form):

        form.save

        return super(UserCreate, self).form_valid(form)
