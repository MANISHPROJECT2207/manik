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
    unit = models.IntegerField(default=0, blank=False)
    subject = models.ForeignKey(Subject, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    link = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=item_status, max_length=15, default="pending")
    completed = models.BooleanField(default=False)
    completed_by = models.ManyToManyField(User, related_name='completed_items', blank=True)
    revision = models.BooleanField(default=False)
    revision_by = models.ManyToManyField(User, related_name='revision_items', blank=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_items', blank=True)
    
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        unit, created = Unit.objects.get_or_create(
            number=self.unit,
            subject=self.subject,
            defaults={'name': self.subject.name}
        )
        unit.items.add(self)
        unit.save()
    
class Unit(models.Model):
    subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='units')
    number = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_by = models.ManyToManyField(User, related_name='completed_units', blank=True)
    name = models.CharField(max_length=255, default=subject.name)
    
    def __str__(self):
        return str(self.number)
    
class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profiles', on_delete=models.CASCADE)
    pfp = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    year = models.IntegerField(default=0)
    branch = models.CharField(choices=Branches, max_length=30, default="Common")
        
    def __str__(self):
        return self.user.email
    
class Feedback(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name='feedbacks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username