from django.urls import path, include

from . import views

app_name = "todoapp"
urlpatterns = [
    path("", views.TodoListView.as_view(), name="todo_list"),
    path("create-todo/", views.TodoCreateView.as_view(), name="create_todo"),
    path("update-todo/<int:pk>/", views.TodoUpdateView.as_view(), name="update_todo"),
    path("delete-todo/<int:pk>/", views.TodoDeleteView.as_view(), name="delete_todo"),
    path("todo/<int:pk>/", views.TodoDetailView.as_view(), name="todo_detail"),
    path("logout/", views.log_out, name="logout"),
    path("login/", views.log_in, name="login"),
    path("signup/", views.signup, name="signup"),
    path("api/", include("todoapp.api.urls")),
]
