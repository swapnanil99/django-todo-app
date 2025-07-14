from django.db import models
from django.contrib.auth.models import User

class TODOO(models.Model):
    srno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class UserProfile(models.Model):
    ICON_CHOICES = [
        ("user0.png", "User 0"),
        ("user1.png", "User 1"),
        ("user2.png", "User 2"),
        ("user3.png", "User 3"),
        ("user4.png", "User 4"),
        ("user5.png", "User 5"),
        ("user6.png", "User 6"),
        # Add more icon files if you want
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_icon = models.CharField(max_length=100, choices=ICON_CHOICES, default='icon1.png')

    def __str__(self):
        return self.user.username