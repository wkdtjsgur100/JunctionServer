from django.db import models


# Create your models here.
class Place(models.Model):
    STATUS_CHOICES = (
        ('red', 'red'),
        ('yellow', 'yellow'),
        ('green', 'green'),
    )

    aito_id = models.CharField(max_length=255, default='1')
    latitude = models.FloatField()
    longitude = models.FloatField()
    the_geom_meter = models.CharField(max_length=512)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    fax = models.CharField(max_length=256)
    zip = models.CharField(max_length=256)
    alcohol = models.CharField(max_length=256)
    smoking_area = models.CharField(max_length=256)
    dress_code = models.CharField(max_length=256)
    accessibility = models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    Rambience = models.CharField(max_length=256)
    franchise = models.CharField(max_length=4)
    area = models.CharField(max_length=256)
    other_services = models.CharField(max_length=256)
    wifi = models.BooleanField(default=False)
    sockets = models.BooleanField(default=False)
    workspace = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    congestion = models.CharField(max_length=16, choices=STATUS_CHOICES, default='green')


class UserLike(models.Model):
    is_super_like = models.BooleanField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    user_id = models.IntegerField()


class PaymentAccepts(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    payment = models.CharField(max_length=64)


class Cuisine(models.Model):
    name = models.CharField(max_length=255)