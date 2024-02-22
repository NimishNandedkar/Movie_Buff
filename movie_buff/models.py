from django.db import models
from django.contrib.auth.models import User


from django.core.validators import RegexValidator
from django.db.models.signals import post_save 
from django.dispatch import receiver
from PIL import Image

# Create your models here.

    
class movie_detail(models.Model):
    movie_name =  models.CharField(max_length=50)   
    genre= models.CharField(max_length=15,choices=[('science_fiction', 'Science Fiction'), ('action', 'Action'),('horror', 'Horror'),('thriller', 'Thriller'),('animated', 'Animated')])  
    desc= models.CharField(max_length=500)
    poster=models.ImageField(upload_to='movie_buff/posters')
    video= models.FileField(upload_to='movie_buff/videos')

    #changes made in model field on 22/10/23
    
    actors =  models.CharField(max_length=100,blank=True)
    CBFC_certificate  = models.CharField(max_length=5, choices=[('U', 'U'), ('U/A', 'U/A'), ('A', 'A'),('S', 'S')],null=True, blank=True)
    movie_duration = models.CharField(max_length=10, blank=True)

   

    NEW_RELEASES = models.BooleanField(default=False)


    #below code for to add like field is created on 20/10/23 yesterday
     # New fields for tracking likes and dislikes
    likes = models.ManyToManyField(User, related_name='liked_movies',blank=True)   #changes made on 22/10/23
    
    def __str__(self):
        return self.movie_name 
    
    def num_likes(self):
        return self.likes.count()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.poster.path)

        if img.height> 300 or img.width>300:
            output_size= (1080,1080)
            img.thumbnail(output_size)
            img.save(self.poster.path)


class WatchLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(movie_detail, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.video.movie_name}"


#below code for user profile is created on 20/10/23 yesterday

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone_number =models.CharField( max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    session_token = models.CharField(max_length=50, blank=True, null=True)
   
    profile_picture= models.ImageField(default='user.png' , upload_to='profilepics/')


    browser_name = models.CharField(max_length=10,blank=True, null=True)
    os_name = models.CharField(max_length=10,blank=True, null=True)
    device_name = models.CharField(max_length=10,blank=True, null=True) 

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height> 300 or img.width>300:
            output_size= (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)




@receiver(post_save , sender=User)
def user_is_created( sender , instance , created , **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

    else:
        instance.userprofile.save()    

       