import os
import uuid
from PIL import Image
from django.contrib.auth.models import User

from django.db import models

class UserVoteStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote status for {self.user.username}"


# Create your models here.
def upload_location(instance, filename):
    ext = filename.split('.')[-1]
    name = uuid.uuid4()
    full_name = f'{name}.{ext}'
    return os.path.join('candidates_images', full_name)


class Candidate(models.Model):
    POSITION_CHOICES = [
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Finance Secretary', 'Finance Secretary'),
        ('Academic Secretary', 'Academic Secretary'),
        ('Delegate', 'Delegate'),

    ]
    PARTY_CHOICES = [
        ('Umoja', 'Umoja'),
        ('Maendeleo', 'Maendeleo'),
        ('Utumishi', 'Utumishi'),
        ('Mfalme', 'Mfalme'),
    ]
    full_name = models.CharField(max_length=150)
    party = models.CharField(max_length=50, choices=PARTY_CHOICES)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    votes = models.IntegerField(default=0)
    image = models.ImageField(upload_to=upload_location)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name}-{self.position}'

    def save(self, *args, **kwargs):
        super(Candidate, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)