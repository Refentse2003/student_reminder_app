from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def is_due_soon(self):
        return (self.due_date - date.today()).days <= 1

    def __str__(self):
        return self.title
