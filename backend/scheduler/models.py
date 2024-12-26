from django.db import models

class Feedback(models.Model):
    career = models.CharField(max_length=255)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.career} - {self.rating}"
