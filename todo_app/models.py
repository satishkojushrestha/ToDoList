from django.db import models

class Usersa(models.Model):
    username = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id} : {self.username}"

class UserDetail(models.Model):
    user = models.ForeignKey(Usersa, on_delete=models.CASCADE, related_name="userinfo")
    task = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user} : {self.task}"

