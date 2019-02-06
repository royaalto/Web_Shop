from django.db import models
from django.contrib.auth.models import User




def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)



class Category(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name


'''
Model for Games
'''
class Game(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=200, unique=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    image2 = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    available = models.BooleanField(default=False)
    category = models.ManyToManyField(Category,verbose_name='Category')
    release_date = models.DateField(null=True)
    score_board = models.BooleanField(default=False)
    sold_qty = models.PositiveIntegerField(default =0)
    revenue = models.DecimalField(default =0,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name

