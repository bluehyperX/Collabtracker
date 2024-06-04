from django.db import models

# Create your models here.
class Employee (models.Model):
    name = models.CharField(max_length = 255, blank = False)
    # lastname = models.CharField(max_length = 255, blank = False)
    # email = models.CharField(max_length = 255, blank = False, primary_key = True)

    def __str__(self):
        return f"Name: {self.name}"
