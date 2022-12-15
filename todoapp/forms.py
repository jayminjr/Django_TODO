from django import forms
from . import models
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LogInForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class TodoForm(forms.ModelForm):
    class Meta:
        model = models.Todo
        fields = "__all__"
        exclude = ["user"]
        widgets = {"due_date": widgets.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
