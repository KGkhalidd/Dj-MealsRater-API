import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Meal(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(meal=self).count()
        return ratings
    
    def avg_rating(self):
        return Rating.objects.filter(meal=self).aggregate(Avg('stars'))['stars__avg'] or 0

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Rating(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stars} stars for {self.meal}"
    
    class Meta:
        ordering = ['-created']
        unique_together = (('user', 'meal'),)
        index_together = (('user', 'meal'),)