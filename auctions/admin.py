from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Auction, Bid, Comment, Watchlist

admin.site.register(User, UserAdmin)

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'base_price', 'category', 'user','is_active', 'slug', 'updated')
    list_filter = ('title', 'category', 'is_active')
    search_fields = ('title', )
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-updated',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Bid)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'auction',  'user', 'bid')
    list_filter = ('auction', 'user')
    search_fields = ('auction', 'user')
    ordering = ('-auction', '-bid')

@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'auction',  'user')
    list_filter = ('auction', 'user')
    search_fields = ('auction', 'user')
    ordering = ('-auction',)

@admin.register(Watchlist)
class Categorydmin(admin.ModelAdmin):
    list_display = ('id', 'auction',  'user', 'created')
    list_filter = ('auction', 'user')
    search_fields = ('auction', 'user')
    ordering = ('-auction', '-created')

