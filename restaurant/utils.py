
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
# 문장에서 명사를 추출하는 형태소 분석 라이브러리
import jpype
from konlpy.tag import Hannanum
import io, os, sys
import base64
from restaurant.models import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
font_path = os.path.join('restaurant/static/fonts/D2Coding-Ver1.3.2-20180524.ttc')

def make_wordcloud(reviews_text, font_path):
    if not reviews_text.strip():  
        return None
    else:
        # 형태소 분석을 통해 명사 추출
        hannanum = Hannanum()
        nouns = hannanum.nouns(reviews_text)
        words = [noun for noun in nouns if len(noun) > 1]
        
        # WordCloud 생성
        wordcloud = WordCloud(
            font_path= font_path,
            background_color='white',
            width=500,
            height=500
        ).generate(','.join(words))  # 텍스트(빈도 1 초과인 명사)로부터 단어 클라우드 생성

        # 이미지로 저장
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')  # 축을 숨김
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return image_base64


def make_chef_json(chef_instance):
    """
        < json구조 >
        chef_json = {
            "chef_name" : 
            "image_url" :
            "restaurants" : [
                {
                    "restaurant_name": 
                    "address": 
                    "style": 
                    "url": 
                    "review_count": ,
                    "description": 
                    "menus": [{"menu_name":~~, "price":~~}, {"menu_name":~~, "price":~~}],
                    "reviews": {"good_reviews": Object, "baed_reviews" : Object},
                    "bar_plot": Object
                },
                {
                    "restaurant_name": 
                    "address": 
                    "style": 
                    "url": 
                    "review_count": ,
                    "description": 
                    "menus": [{"menu_name":~~, "price":~~}, {"menu_name":~~, "price":~~}],
                    "reviews": {"good_reviews": Object, "baed_reviews" : Object},
                    "bar_plot": Object
                }
            ]
        }    
------------------------------------------------------------
    menus = [{"menu_name":~~, "price":~~}]
    reviews = {"good_reviews": Object, "baed_reviews" : Object}
    bar_plot = bar graph
    """

    # 기본 구조 설정
    chef_json = {
        "chef_name": chef_instance.chef_name,
        "image_url": chef_instance.image_url,
        "restaurants": []
    }

    # 레스토랑별 메뉴, 리뷰 워드클라우드 생성
    for restaurant in chef_instance.restaurants.all():     
        menus = []
        reviews = []
        for menu in restaurant.menus.all():
            menus.append(
                {"menu_name": menu.menu_name,
                 "price" : string_to_amount(menu.price)}
            )
        good_reviews_text = ""
        bad_reviews_text = ""
        # 좋은 리뷰와 안 좋은 리뷰 확인
        for good_review in restaurant.reviews.filter(review_category='good'):
            good_reviews_text += good_review.review_text+' '
        for bad_review in restaurant.reviews.filter(review_category='bad'):
            bad_reviews_text += bad_review.review_text+' '
        reviews.append(make_wordcloud(good_reviews_text, font_path))
        reviews.append(make_wordcloud(bad_reviews_text, font_path))
        font_prop = font_manager.FontProperties(fname=font_path)

        fig, ax = plt.subplots(figsize=(5,5))

        total_sum_price = 0
        total_sum_size = Menu.objects.values('price').count()
        for string_price in Menu.objects.values('price'):
            if string_price['price'].strip() == '':
                total_sum_size-=1
                continue
            total_sum_price += string_to_amount(string_price['price'])

        this_sum_price = 0
        this_sum_size = restaurant.menus.all().count()
        for string_price in restaurant.menus.values('price'):
            if string_price['price'].strip() == '':
                this_sum_size-=1
                continue
            this_sum_price += string_to_amount(string_price['price'])         
        
        mean_restaurant_price = total_sum_price // total_sum_size
        this_restaurant_price = this_sum_price  // (this_sum_size if this_sum_size > 0 else 1)


        bar_plot = ax.bar(['평균 가격', '이 식당의 평균 가격'], [mean_restaurant_price, this_restaurant_price], color=['#4CAF50', '#F44336'])
        ax.set_xticklabels(['평균 가격', '이 식당의 평균 가격'], fontproperties=font_prop)
        ax.set_title('가격 수', fontproperties=font_prop)
        ax.set_ylabel('가격', fontproperties=font_prop)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
        #plot_base64 = "바그래프"
        restaurant_data = {
            "restaurant_name": restaurant.restaurant_name,
            "address": restaurant.address,
            "style": restaurant.style,
            "url": restaurant.url,
            "review_count": restaurant.review_count,
            "description": restaurant.description,
            "menus": menus,
            "reviews": reviews,
            "bar_plot": plot_base64
        }
        chef_json["restaurants"].append(restaurant_data)

    return chef_json

def string_to_amount(s):
    if s.strip() == '':
        return 0
    won = []
    for price_word in s.split(' - '):
        price_word = price_word.replace(",", "")
        price_word = price_word.replace("원", "")
        won.append(int(price_word))
    if len(won) == 0:
        return 0
    else:
        return int(sum(won)/len(won))