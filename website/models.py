from django.db import models
from django.contrib.auth.models import User

item_status = [
    ("pending","Pending"),
    ("completed","Completed")
]

revision_status = [
    ("not visited", "Not Visited"),
    ("revision", "Revision")
]

Branches = [
    ("Common", "common/all"),
    ("CSE.", "computer science and engg"),
    ("EC.","electronics and comm."),
    ("Elec.","electrical"),
    ("IT.", "information technology"),
    ("Mech.", "mechanical"),
    ("Civil", "civil"),
    ("AI.", "Artificial Intelligence"),
]

class Subject(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField(default=0)
    branch = models.CharField(choices=Branches, max_length=30, default="Common")
    views = models.IntegerField(default=0)
    viewed_by = models.ManyToManyField(User, related_name='viewed_subjects', blank=True)
    
    def __str__(self):
        return (f"{self.name}, {self.branch}")
    
class Item(models.Model):
    subject = models.ForeignKey(Subject, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    link = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=item_status, max_length=15, default="pending")
    revision = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_items', blank=True)
    
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        return self.title