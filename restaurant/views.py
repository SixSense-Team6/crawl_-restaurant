from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
import jpype
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from wordcloud import WordCloud

# 문장에서 명사를 추출하는 형태소 분석 라이브러리
from konlpy.tag import Hannanum
import io, os
import base64

from .utils import make_wordcloud, avg_price_plot, menu_price_plot



def index(request):
    chefs = Chef.objects.all().values()
    return render(request, 'restaurant/index.html', {'chefs':chefs})

def detail(request, chef_id):
    font_path = os.path.join(settings.BASE_DIR, 'restaurant', 'static', 'fonts', 'D2Coding-Ver1.3.2-20180524.ttc')
    chef = get_object_or_404(Chef, pk=chef_id)
    chef_json = {
        'chef_name' : chef.chef_name,
        'image_url' : chef.image_url
    }

    good_reviews_text = ""
    bad_reviews_text = ""
    # 좋은 리뷰와 안 좋은 리뷰 확인
    for restaurant in chef.restaurants.all():
        for good_review in restaurant.reviews.filter(review_category='good'):
            good_reviews_text += good_review.review_text+' '
        for bad_review in restaurant.reviews.filter(review_category='bad'):
            bad_reviews_text += bad_review.review_text+' '
    
    chef_json['word_cloud_good'] = make_wordcloud(good_reviews_text, font_path)
    chef_json['word_cloud_bad'] = make_wordcloud(bad_reviews_text, font_path)

    # 가격 평균 보여주기
    mean_restaurant_price = 100000
    this_restaurant_price = 50000
    chef_json['bar_plot'] = avg_price_plot(mean_restaurant_price, this_restaurant_price, font_path)  # Base64 문자열 저장
    
    # 메뉴 가격
    menu = ["딤섬 SET", "티엔 SET", "미미 SET", "여명 SET", "티엔미미철판볶음", "어향완자가지", "마라크림새우", "철판 유산슬", "배추찜", "산라탕"]
    price = [40000, 50000, 70000, 100000, 47000, 39000, 36000, 41000, 38000, 38000]
    menu_price_bar_plot = menu_price_plot(menu, price, font_path)
    
    return render(request, 'restaurant/detail.html', {'chef_info': chef_json})


