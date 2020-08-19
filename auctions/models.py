from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

#Custom Manager to filter active auctions
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.CharField(max_length=120, blank=True)
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="auctions", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("detail", args=[self.slug])
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created',)

    objects = models.Manager()
    active = ActiveManager()


class Bid(models.Model):
    bid = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, related_name="bid", on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name="bid", on_delete=models.CASCADE)

    def __str__(self):
        return f'Bid for ${self.bid} on {self.auction} by {self.user}'
        

class Comment(models.Model):
    body = models.TextField()
    auction = models.ForeignKey(Auction, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.auction}'

    class Meta:
        ordering = ('created',)


class Watchlist(models.Model):
    user = models.ForeignKey(User, related_name="watchlist", on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name="watchlist", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.auction} watched by {self.user.username}'

    class Meta:
        ordering = ['-created']
        unique_together = ['user', 'auction']