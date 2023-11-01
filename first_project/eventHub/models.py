from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image 

# Model for representing an event
class Event(models.Model):
    title = models.CharField(max_length=150, default="Default Title")
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=150, default="Default Location")
    description = models.TextField(default="No description available")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


# Model for representing a user profile    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        # Resize and save profile images
        img = Image.open(self.image.path)

        if img.height > 250 or img.width > 250:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.image.path)


# Model for representing attendees at an event
class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    