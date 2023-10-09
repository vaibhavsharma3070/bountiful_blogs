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
    
    def save(self, *args, **kwargs):
        if self.id is not None:
            ReviewLogs.objects.create(user=self.created_by,action="UPDATE",modelname=f"Settings updated by {self.created_by}")
        else:
            ReviewLogs.objects.create(user=self.created_by,action="INSERT",modelname=f"Settings added by {self.created_by}")
        super(Settings,self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        model_name = self.__class__.__name__
        mod_name=f"Model Name->{model_name} | User->{self.created_by}"
        ReviewLogs.objects.create(user=self.created_by,action="DELETE",modelname=f"settings deleted by {self.created_by}")

        super(Settings, self).delete(*args, **kwargs)

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
    
    def save(self, *args, **kwargs):
        if self.id is not None:
            ReviewLogs.objects.create(user=self.created_by,action="UPDATE",modelname=f"Project {self.name} updated by {self.created_by}")

        else:
            ReviewLogs.objects.create(user=self.created_by,action="INSERT",modelname=f"Project {self.name} updated by {self.created_by}")
        super(Project,self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        ReviewLogs.objects.create(user=self.created_by,action="DELETE",modelname=f"Project {self.name} deleted by {self.created_by}")
        super(Project, self).delete(*args, **kwargs)


class ProjectImages(models.Model):
    parent_model = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')


class Batch(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return self.name

    def save(self, *args, **kwargs):
        model_name = self.__class__.__name__
        mod_name=f"Model Name->{model_name} | Batch Name->{self.name}"
        if self.id is not None:
            ReviewLogs.objects.create(user=self.created_by,action="UPDATE",modelname=f"Batch {self.name} updated by {self.created_by}")
        else:
            ReviewLogs.objects.create(user=self.created_by,action="INSERT",modelname=f"Batch {self.name} created by {self.created_by}")
        super(Batch,self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        model_name = self.__class__.__name__
        mod_name=f"Model Name->{model_name} | Batch Name->{self.name}"
        ReviewLogs.objects.create(user=self.created_by,action="DELETE",modelname=f"Batch {self.name} deleted by {self.created_by}")
        super(Batch, self).delete(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'project')


class Article(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    old_article = models.FileField(upload_to='old_articles/', null=True, blank=True)
    new_article = models.FileField(upload_to='new_articles/', null=True, blank=True)
    html_file=models.FileField(upload_to='',null=True,blank=True)
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

    def save(self, *args, **kwargs):
        model_name = self.__class__.__name__
        if self.id is not None:
            ReviewLogs.objects.create(user=self.created_by,action="UPDATE",modelname=f"Article updated by {self.created_by}")
        else:
            ReviewLogs.objects.create(user=self.created_by,action="INSERT",modelname=f"Article created by {self.created_by}")
        super(Article,self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        model_name = self.__class__.__name__
        ReviewLogs.objects.create(user=self.created_by,action="DELETE",modelname=f"Article deleted by {self.created_by}")
        super(Article, self).delete(*args, **kwargs)


class ReviewLogs(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    action=models.CharField(max_length=20)
    modelname=models.CharField(max_length=100)