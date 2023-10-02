from django.db import models
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class Settings(models.Model):
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    openai_key = models.CharField(max_length=255)
    envato_key = models.CharField(max_length=255)
    min_image = models.PositiveIntegerField()
    max_size = models.PositiveIntegerField()
    search_tags = models.PositiveIntegerField()
    h2_start_from = models.PositiveIntegerField()
    api_delay = models.PositiveIntegerField()
    image_width = models.FloatField()
    block_quote_per_article = models.PositiveIntegerField()
    bolded_quote_per_article = models.PositiveIntegerField()
    image_prompt = models.TextField()
    block_quote = models.TextField()

    def __str__(self) -> str:
        return self.created_by.username

class Project(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    url = models.TextField()
    image_website = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    def get_images(self):
        return ProjectImages.objects.filter(parent_model=self)


class ProjectImages(models.Model):
    parent_model = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')


class Batch(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return self.name
    
    class Meta:
        unique_together = ('name', 'project')


class Article(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    old_article = models.FileField(upload_to='old_articles/', null=True, blank=True)
    new_article = models.FileField(upload_to='new_articles/', null=True, blank=True)
    search_tags = models.BooleanField(default=False)
    image_tags = models.BooleanField(default=False)
    old_json = models.TextField(null=True, blank=True, default=dict)
    new_json = models.TextField(null=True, blank=True, default=dict)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @staticmethod
    def is_json(data):
        try:
            json.loads(data)
        except ValueError:
            return False
        return True

    def set_old_json(self, data):
        self.old_json = json.dumps(data)

    def get_old_json(self):
        return json.loads(self.old_json)

    def set_new_json(self, data):
        self.new_json = json.dumps(data)

    def get_new_json(self):
        return json.loads(self.new_json)

    # def __str__(self) -> str:
    #     return self.name
