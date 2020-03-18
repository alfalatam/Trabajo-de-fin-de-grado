from django.db import models


# Create your models here.


# class ToDoList(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="todolist", null=True)
#     name = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     name = models.CharField(max_length=25)
#     lastName = models.CharField(max_length=25)
#     age = models.IntegerField()

#     def __str__(self):
#         return self.user.username
