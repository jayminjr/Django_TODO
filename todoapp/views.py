from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib import messages

from todoapp.forms import LogInForm, SignUpForm, TodoForm
from .models import Todo

# Create your views here.
class TodoListView(LoginRequiredMixin, ListView):
    """
    A ListView to display all todos
    """

    model = Todo
    context_object_name = "todo_list"
    template_name = "todo_list.html"

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user)


class TodoDetailView(LoginRequiredMixin, DetailView):
    """
    A DetailView to display todo detail
    """

    model = Todo
    template_name = "todo_detail.html"


class TodoCreateView(LoginRequiredMixin, CreateView):
    """
    A CreateView to create todo
    """

    model = Todo
    template_name = "todo_form.html"
    form_class = TodoForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreateView, self).form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    """
    A UpdateView to update todo
    """

    model = Todo
    template_name = "todo_form.html"
    form_class = TodoForm

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    """
    A DeleteView to delete todo
    """

    model = Todo
    template_name = "todo_confirm_delete.html"

    def get_success_url(self):
        return reverse("todoapp:todo_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def log_out(request):
    """
    Handle logout operation
    """
    logout(request)
    messages.success(request, "Logged out.")
    return redirect(reverse("todoapp:todo_list"))


def log_in(request):
    """
    Handle authenticate and login operation
    """
    if request.user.is_authenticated:
        return redirect("todoapp:todo_list")
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in.")
                return redirect("todoapp:todo_list")
    else:
        form = LogInForm()
    return render(request, "login.html", {"form": form})


def signup(request):
    """
    Handle signup operation
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("todo_list")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})
