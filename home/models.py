from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Settings(models.Model):
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    openai_key = models.CharField(max_length=255)
    envato_key = models.CharField(max_length=255)
    min_image = models.IntegerField()
    max_size = models.IntegerField()
    search_tags = models.IntegerField()
    h2_start_from = models.IntegerField()
    api_delay = models.IntegerField()
    image_width = models.FloatField()
    block_quote_per_article = models.IntegerField()
    bolded_quote_per_article = models.IntegerField()
    image_prompt = models.TextField()
    block_quote = models.TextField()

    def __str__(self) -> str:
        return self.created_by.username

class Project(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    url = models.TextField()
    image_folder = models.CharField(max_length=100, null=True, blank=True)
    image_website = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    def to_json(self):
        # Convert the Project object to a dictionary that can be serialized to JSON
        return {
            'created_by': self.created_by,
            'name': self.name,
            'url': self.url,
            'image_folder': self.image_folder,
            'image_website': self.image_website
        }


class Article(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    batch = models.CharField(max_length=100)
    search_tags = models.BooleanField(default=False)
    image_tags = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
