from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.auth import get_user_model


UserModel = get_user_model()
# Create your models here.
class Todo(models.Model):
    CATEGORY_CHOICES = (
        ("normal", "Normal"),
        ("important", "Important"),
        ("urgent", "Urgent"),
    )
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    category = models.CharField(
        _("category"), max_length=50, choices=CATEGORY_CHOICES, default="normal"
    )
    due_date = models.DateField(_("Due Date"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("todoapp:todo_detail", args=[self.pk])
