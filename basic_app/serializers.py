import requests
from django.contrib.auth import get_user_model
from rest_framework import serializers

from basic_app.models import Product, ProductCategory, ProductShots, About, BestSellerProducts, WorksByKaleGalleryShots, \
    WorksByKaleGallery, InfoGrafika, GalleryOnlyImages, Partners, Gallery_News, Form, SocialNetworks, Location, \
    WorksByKale, Discount, BarabanDiscount, Orders, Header_Carusel, TopProductShots, TopProductCategory, TopProduct, \
    ChatRoom, ChatMessage, MyObjects, ModelObjects, ProductWorksByCompany, UsedProductsInWorksKale
from conf.settings import BOT_TOKEN

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


def telebot(mess):
    requests.get(
        url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={GROUP_CHAT_ID}&parse_mode=HTML&text={mess}")


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name_uz', 'name_ru', 'name_en']


class ProductShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductShots
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    images = ProductShotsSerializer(source='productshots_set', many=True)

    class Meta:
        model = Product
        fields = '__all__'


class WorksByCompanyShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductWorksByCompany
        fields = ['image']


class UsedProductsInWorksKaleSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = UsedProductsInWorksKale
        fields = '__all__'


class WorksByKaleSerializer(serializers.ModelSerializer):
    images = WorksByCompanyShotsSerializer(source='productworksbycompany_set', many=True)
    used_products = UsedProductsInWorksKaleSerializer(many=True)

    class Meta:
        model = WorksByKale
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'


class BestSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BestSellerProducts
        fields = '__all__'


class WorksByKaleGalleryShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorksByKaleGalleryShots
        fields = ('id', 'image')


class WorksByKaleGallerySerializer(serializers.ModelSerializer):
    # images = WorksByKaleGalleryShotsSerializer(many=True, read_only=True)
    images = ProductShotsSerializer(source='worksbykalegalleryshots_set', many=True)

    class Meta:
        model = WorksByKaleGallery
        # fields = ('id', 'title_uz', 'title_en', 'title_ru', 'text_uz', 'text_en', 'text_ru', 'images')
        fields = '__all__'


class InfografikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoGrafika
        fields = '__all__'


class GalleryOnlyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryOnlyImages
        fields = '__all__'


class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = '__all__'


class Gallery_NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery_News
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'name', 'phone', 'address']

    def create(self, validated_data):
        # Create the object using the validated data
        my_object = Form.objects.create(**validated_data)

        # Send a message to the Telegram group
        message = f"New User: \n\n{my_object}"
        telebot(message)
        return my_object


class SocialNetworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetworks
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

    def create(self, validated_data):
        # Create the object using the validated data
        my_object = Discount.objects.create(**validated_data)

        # Send a message to the Telegram group
        message = f"New User: \n\n{my_object}"
        telebot(message)
        return my_object


class BarabanDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarabanDiscount
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

    def create(self, validated_data):
        # Create the object using the validated data
        my_object = Orders.objects.create(**validated_data)

        # Send a message to the Telegram group
        message = f"New User: \n\n{my_object}"
        telebot(message)
        return my_object


class HeaderCaruselSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Header_Carusel
        fields = ['id', 'nomi_uz', 'nomi_ru', 'nomi_en',
                  'text_uz', 'text_ru', 'text_en',
                  'image']

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        else:
            return None


class TopProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TopProductCategory
        fields = ['id', 'name_uz', 'name_ru', 'name_en']


class TopProductShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopProductShots
        fields = ['image']


class TopProductSerializer(serializers.ModelSerializer):
    category = TopProductCategorySerializer()
    images = TopProductShotsSerializer(source='topproductshots_set', many=True)

    class Meta:
        model = TopProduct
        fields = '__all__'


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'


class ModelObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelObjects
        fields = '__all__'


class MyObjectsSerializer(serializers.ModelSerializer):
    object = ModelObjectsSerializer()

    class Meta:
        model = MyObjects
        fields = ['key', 'object']

    def create(self, validated_data):
        object_data = validated_data.pop('object')
        model_object = ModelObjects.objects.create(**object_data)
        my_object = MyObjects.objects.create(object=model_object, **validated_data)
        return my_object


