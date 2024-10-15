from django.contrib import admin
from .models import Chef, Restaurant, Review, Menu

@admin.register(Chef)
class Chef(admin.ModelAdmin):
    list_display = ('chef_name', 'image_url')  # 표시할 필드 설정
    search_fields = ('chef_name',)  # 검색 가능 필드 설정

@admin.register(Restaurant)
class Restaurant(admin.ModelAdmin):
    list_display = ('chef', 'restaurant_name')  # 표시할 필드 설정
    search_fields = ('chef',)  # 검색 가능 필드 설정

@admin.register(Review)    
class Review(admin.ModelAdmin):
    list_display = ('restaurant', 'review_text', 'review_category')  # 표시할 필드 설정
    search_fields = ('restaurant',)  # 검색 가능 필드 설정

@admin.register(Menu)
class Menu(admin.ModelAdmin):
    list_display = ('restaurant', 'menu_name', 'price')  # 표시할 필드 설정
    search_fields = ('restaurant',)  # 검색 가능 필드 설정