from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BackgroundTasks(models.Model):
    domain_name = models.CharField(max_length=50, null=True)
    keyword = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=50, null=True)
    date = models.DateField(null=True)
    def update_status(self, status):
        self.state = status
        self.save()

class Tags(models.Model):
    name = models.CharField(max_length=255, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, null=True)

class Response(models.Model):
    background_task_id = models.IntegerField(null=True)
    keyword = models.CharField(max_length=255, null=True)
    email = models.TextField(null=True)
    response_object = models.TextField(null=True)
    domain_name = models.CharField(max_length=50, null=True)
    name = models.TextField(null=True)
    industry = models.TextField(null=True)
    designation = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TaggedResponses(models.Model):
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('tag', 'response')

class Results(models.Model):
    domain_name = models.TextField()
    keyword = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
