from yandex_search.yandex_search_1 import run_query
from vil_app.models import Category, Page, UserProfile
from vil_app.forms import UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic, View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.http import HttpResponse

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
# def search(request, slug):
#
#     context_dict = {}
#     if request.method == 'POST':
#         category = Category.objects.get(slug=slug)
#         context_dict['categorias'] = category
#         query = request.POST['query'].strip()
#         if query:
#             context_dict['result_list'] = run_query(query)
#             context_dict['query'] = query
#
#
#     return render(request, 'vil_app/show_pages.html', context_dict)
# def post(self, request, slug):
#         context_dict = self.create_context_dict(slug)
#         query = request.POST['query'].strip()
#
#         if query:
#             context_dict['result_list'] = run_query(query)
#             context_dict['query'] = query
#
#         return render(request, 'vil_app/show_pages.html', context_dict)

class ShowCategoryView(View):
    def create_context_dict(self, slug):
        """
        A helper method that was created to demonstrate the power of class-based views.
        You can reuse this method in the get() and post() methods!
        """
        context_dict = {}

        try:
            category = Category.objects.get(slug=slug)
            pages = Page.objects.filter(category=category)

            context_dict['pages'] = pages
            context_dict['categorias'] = category
        except Category.DoesNotExist:
            context_dict['category'] = None
            context_dict['pages'] = None

        return context_dict

    def get(self, request, slug):
        context_dict = self.create_context_dict(slug)
        return render(request, 'vil_app/show_pages.html', context_dict)

    def post(self, request, slug):
        context_dict = self.create_context_dict(slug)
        query = request.POST['query'].strip()

        if query:
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query

        return render(request, 'vil_app/show_pages.html', context_dict)


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


# class ShowpagesDetailView(generic.DetailView):
#     model = Category
#     # queryset = Category.objects.get(slug=pk)
#     context_object_name = 'categorias'
#     template_name = 'vil_app/show_pages.html'


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ('name', )
    # success_url = reverse_lazy('index')

    def get_success_url(self):
        return reverse_lazy('vil_app:categoria', kwargs={'slug': self.object.slug})


class PageCreate(LoginRequiredMixin, CreateView):
    model = Page
    fields = ('title', 'url')
    # success_url = reverse_lazy('index')

    def form_valid(self, form):

        page = form.save(commit=False)

        page.category = get_object_or_404(Category,

                                          slug=self.kwargs.get('slug'))
        page.created_by = self.request.user

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


# class UserCreate(CreateView):
#     model = User
#     form_class = UserCreationForm
#     template_name = 'registration/registracion.html'
#     success_url = reverse_lazy('index') # prox: al user profile
#
#     def form_valid(self, form):
#
#         form.save
#
#         return super(UserCreate, self).form_valid(form)


class UserCreate(View):
    def get(self, request):
        form = UserCreationForm()
        context_dict = {'form': form}
        return render(request, 'registration/registracion.html', context_dict)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
            login(request, user)

            return redirect('vil_app:profile', username=user.username)
        else:
            print(form.errors)

        context_dict = {'form': form}
        return render(request, 'registration/registracion.html', context_dict)


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('index')

        userprofile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': userprofile.website,
                                'picture': userprofile.picture})
        return(user, userprofile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        (user, userprofile, form) = self.get_user_details(username)
        return render(request, 'vil_app/profile.html',
                               {'userprofile': userprofile,
                                   'selecteduser': user,
                                   'form': form})

    @method_decorator(login_required)
    def post(self, request, username):
        (user, userprofile, form) = self.get_user_details(username)
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('vil_app:profile', username=username)
            # reverse_lazy('vil_app:profile', kwargs={'username': self.kwargs['username']})
        else:
            print(form.errors)

        return render(request, 'vil_app/profile.html',
                      {'userprofile': userprofile,
                       'selecteduser': user,
                       'form': form})


class SearchAddPageView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET['category_id']
        title = request.GET['title']
        url = request.GET['url']

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse('Error - category not found.')
        except ValueError:
            return HttpResponse('Error - bad category ID.')

        p = Page.objects.get_or_create(category=category,
                                       title=title,
                                       url=url,
                                       created_by=request.user)

        pages = Page.objects.filter(category=category)
        return render(request, 'vil_app/page_listing.html', {'pages': pages})
