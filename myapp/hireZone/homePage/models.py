from django.db import models
from django.contrib.auth.models import User
import requests

class SeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    skill_set = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    num_ratings = models.PositiveIntegerField(default=0)
    about_me = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(('Profile Photo'), upload_to='profile_photos/', blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.location:
            self.latitude, self.longitude = self._get_lat_long(self.location)
        super(SeekerProfile, self).save(*args, **kwargs)

    def _get_lat_long(self, location):
        base_url = 'https://nominatim.openstreetmap.org/search'
        params = {'q': location, 'format': 'json'}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
        return None, None

    def __str__(self):
        return f'{self.user.username} Profile'
