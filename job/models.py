from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator, MaxValueValidator
import geocoder
import os

# Create your models here.

class JobType(models.TextChoices):
    Pernament = 'Pernament'
    Temporary = 'Temporary'
    Intership = 'Intership'

class Education(models.TextChoices):
    Bachelors = 'Bachelors'
    Master = 'Master'
    Phd = 'Phd'

class Industry(models.TextChoices):
    Business = 'Business'
    IT = 'Infomation Technology'
    Banking = 'Banking'
    Education = 'Education/Training'
    Telecommunication = 'Telecommunication'
    Others = 'Others'

class Experience(models.TextChoices):
    NO_EXPERIENCE = 'No Experience'
    ONE_YEAR = '1 year'
    TWO_YEAR = '2 years'
    THREE_YEAR_PLUS = '3 years above'
    
def return_date_time():
    now = datetime.now()
    return now + timedelta(days=10)

class Job(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=200, null=True)
    jobType = models.CharField(
        max_length=200,
        choices=JobType.choices,
        default=JobType.Pernament
    )
    education = models.CharField(
        max_length=200,
        choices=Education.choices,
        default=Education.Bachelors
    )
    industry = models.CharField(
        max_length=200,
        choices=Industry.choices,
        default=Industry.Business
    )
    experience = models.CharField(
        max_length=200,
        choices=Experience.choices,
        default=Experience.NO_EXPERIENCE
    )
    salary = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    position = models.IntegerField(default=1)
    company = models.CharField(max_length=100, null=False)
    point = gismodels.PointField(default=Point(0.0, 0.0))
    lastDate = models.DateTimeField(default=return_date_time)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        g = geocoder.mapquest(self.address, key=os.environ.get('GEOCODER_API'))
        
        print(g)
        
        lng = g.lng
        lat = g.lat
        
        self.point = Point(lng, lat)
        super(Job, self).save(*args, **kwargs)
        
class CandidatesApplied(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    resume = models.CharField(max_length=200)
    appliedAt = models.DateTimeField(auto_now_add=True)