from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from MyBlog.models import Article, User, Subscriber, Friends
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from MyBlog.forms import EditForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import AuthorPermissionsMixin,MembersPermissionsMixin
from django.views import generic
from MyBlog.forms import SubscriberForm
from django.core.mail import send_mail


def home(request):
    articles = Article.objects.all().order_by('-timestamp')
    tags = Article.objects.values_list('tags', flat=True)
    members = Article.objects.values_list('members',flat=True)
    status = Article.objects.values_list('status',flat=True)
    paginator = Paginator(articles, 3)  # 3 поста на странице
    page = request.GET.get('page')
    context = {
        'page': page,
        'articles': articles,
        'tags': tags,
        'members': members,
        'status': status
    }
    return render(request, 'blog/home.html', context)


def about(request):
    users = User.objects.all().order_by('username')
    context = {
        'users': users,
    }
    return render(request, 'blog/users.html', context)


def show_article(request, article_id):
     article = get_object_or_404(Article, id=article_id)
     return render(request, 'blog/article.html', {'article': article})


def delete(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        article.delete()
        return HttpResponseRedirect("/MyBlog")
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")


def edit(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        form = EditForm(request.POST, instance=article)
        if request.method == "POST":
            article.title = request.POST.get("title")
            article.text = request.POST.get("text")
            article.preview = request.POST.get("preview")
            article.tags = request.POST.get("tags")
            article.save()
            return HttpResponseRedirect("/MyBlog")
        else:
            return render(request, "blog/edit.html", {"form": form})
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")


def show_user(request, username):
    user_name = get_object_or_404(User, username=username)
    # first_name = (User,first_name=User.first_name)
    # friends = Friends.objects.all(User)
    articles = Article.objects.filter(user=user_name)
    paginator = Paginator(articles, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {

        'user_profile': user_name,
        'articles': articles
    }
    return render(request, 'blog/user.html', context)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/MyBlog/"
    template_name = "blog/register.html"
    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/MyBlog')


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "blog/login.html"
    success_url = "/MyBlog"
    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных
        self.user = form.get_user()
        # Выполняем аутентификацию пользователя
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class AddArticle(CreateView):
    model = Article
    fields = ['title', 'preview', 'text', 'members', 'tags','status']
    template_name = 'blog/add.html'
    success_url = "/MyBlog"


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddArticle, self).form_valid(form)


def home_by_tag(request, tag):
    articles = Article.objects.filter(tags__name__in=[tag])
    paginator = Paginator(articles, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'articles': articles,
        'tag': tag
    }
    return render(request, 'blog/tags.html', context)


def home_by_keyword(request):
    keyword = request.GET['keyword']
    articles = Article.objects.filter(text__icontains=keyword)
    paginator = Paginator(articles, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'articles': articles,
        'keyword': keyword
    }
    return render(request, 'blog/search.html', context)


class PostDetailView(MembersPermissionsMixin,generic.DetailView):
    model = Article
    template_name = 'blog/article.html'






class Subscribe(CreateView):
    model = Subscriber
    fields = ['email']
    template_name = 'blog/subscribe_success.html'
    success_url = '/subscribe_success.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Subscribe, self).form_valid(form)


# def show_users(request):
#     users = User.objects.all().order_by('username')
#     context = {
#         'users': users,
#     }
#     return render(request, 'blog/users.html', context)

def show_users(request):
    users = User.objects.all().order_by('username')

    context = {
        'users': users,
    }
    return render(request, 'blog/about.html', context)


def show_friends(request):
    friend = Friends.objects.get(current_user=request.user)
    friends = friend.users.all()
    arg = {
        'friends': friends
    }
    return render(request, 'blog/users.html', arg)


def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }


def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        curr = 'blog/about.html'
        Friends.make_friend(request.user, new_friend)
    elif operation == 'remove':
        curr = 'blog/users.html'
        Friends.lose_friend(request.user, new_friend)
    return render(request, curr)


def Profile(request):
    model = User
    fields = ['username', 'first_name']
    template_name = 'blog/user.html'
    success_url = "/MyBlog"

    context = {
        'username': User.username,
        'first_name': User.first_name
    }

    return render(request, template_name, context)
