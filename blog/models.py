from django.db import models
from django.contrib.auth.models import User  # Using the default User model

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name    

# Post Model
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", default=1)  # Default user with ID=1
     # Correct reference to the User model

    def __str__(self) -> str:
        return self.title

# Comment Model
class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on {self.post}"
