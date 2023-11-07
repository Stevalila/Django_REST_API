from django.db import models
from users.models import User

class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title
