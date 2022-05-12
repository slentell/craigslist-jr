from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from distutils.command.upload import upload
from logging import PlaceHolder
from unicodedata import category
from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from django.utils.text import slugify
from datetime import date
import string
import random
import uuid

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cat_name = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.cat_name}"

class Posts(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length = 1500)
    price = MoneyField(decimal_places=2, max_digits=8, default_currency='USD', validators=[MinMoneyValidator(0)] )
    location = models.CharField(max_length=100)
    seller = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='images')
    date_listed = models.DateField(default=date.today)
    slug = models.SlugField(null = True, blank = True, unique = True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = self.generate_slug()
        return super().save(*args, **kwargs)
    
    def generate_slug(self, save_to_obj=False, add_random_suffix=True):
        generated_slug = slugify(self.title)
        random_suffix = ''
        if add_random_suffix:
            random_suffix = ''.join([random.choice(string.ascii_letters + string.digits)
            for i in range(5)
            ])
            generated_slug += '-%s' % random_suffix
        if save_to_obj:
            self.slug = generated_slug
            self.save(update_fields=['slug'])
        return generated_slug
    
@receiver(pre_delete, sender=Posts)
def posts_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)