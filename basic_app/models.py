import os

from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductUnitChoices(models.TextChoices):
    M2 = ("м2", "м2")
    PIECE = ("шт", "шт")


class ProductCategory(models.Model):
    name_ru = models.CharField(_("Название категории ru"), max_length=100)
    name_uz = models.CharField(_("Kategoriya nomi uz"), max_length=100, null=True, blank=True)
    name_en = models.CharField(_("Product category en"), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Бренд")
        verbose_name_plural = _("Бренды")

    def __str__(self):
        return self.name_ru


class Product(models.Model):
    title_ru = models.CharField(_("Наименование товара ru"), max_length=255, null=True, blank=True)
    title_uz = models.CharField(_("Tovar nomi uz"), max_length=255, null=True, blank=True)
    title_en = models.CharField(_("Product name en"), max_length=255, null=True, blank=True)
    code = models.CharField(_("Код товара"), max_length=50, null=True, blank=True)
    unit = models.CharField(_("Единица измерения"), choices=ProductUnitChoices.choices,
                            default=ProductUnitChoices.PIECE, max_length=10)
    brand = models.CharField(_("Торговая марка"), max_length=50, null=True, blank=True)
    proportions = models.CharField(_("Размеры"), max_length=30, null=True, blank=True)
    description_ru = models.TextField(_("Описание ru"), null=True, blank=True)
    description_uz = models.TextField(_("Tavsif uz"), null=True, blank=True)
    description_en = models.TextField(_("Description en"), null=True, blank=True)
    manufacturer = models.CharField(_("Производитель"), max_length=20, null=True, blank=True)
    category = models.ForeignKey("basic_app.ProductCategory", on_delete=models.PROTECT, null=True, blank=True)
    rest_count = models.FloatField(_("Остаток товара"), default=0)
    is_float = models.BooleanField(_("Остаток является нецелым"), default=False)
    price = models.IntegerField(_("Цена"), default=0)
    is_deleted = models.BooleanField(_("Удален ли товар"), default=False)
    top_product = models.BooleanField(_("Топ товар"), default=False)

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return self.title_ru if self.title_ru else _("Не заполнено")


class ProductShots(models.Model):
    product = models.ForeignKey("basic_app.Product", on_delete=models.CASCADE)
    image = models.ImageField(_("Изображение"))

    class Meta:
        verbose_name = _("Изображение товара")
        verbose_name_plural = _("Изображения товаров")


    def __str__(self):
        return str(self.image)

    def get_image_file_name(self):
        return os.path.basename(self.image.name)


class ProductUpdateLog(models.Model):
    updated_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["-created_at"]


class About(models.Model):
    image = models.ImageField(upload_to='products/')
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    text_uz = models.TextField(blank=True, null=True, default='matn kiritilmagan')
    text_ru = models.TextField(blank=True, null=True, default='matn kiritilmagan')
    text_en = models.TextField(blank=True, null=True, default='matn kiritilmagan')

    def __str__(self):
        return self.title_ru

    def url(self):
        if self.image:
            return self.image.url
        else:
            return ''

    class Meta:
        verbose_name = _("About")
        verbose_name_plural = _("Abouts")


class BestSellerProducts(models.Model):
    name_uz = models.CharField(max_length=300, default='nomi kiritilmagan', null=True, blank=True)
    name_ru = models.CharField(max_length=300, default='nomi kiritilmagan', null=True, blank=True)
    name_en = models.CharField(max_length=300, default='nomi kiritilmagan', null=True, blank=True)
    description_uz = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    description_ru = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    description_en = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    image = models.ImageField(upload_to='best_seller_images/', null=True, blank=True)
    best_seller_product = models.BooleanField(default=False)
    text_color = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Бестселлер")
        verbose_name_plural = _("Бестселлеры")

    def __str__(self):
        return self.name_ru if self.name_uz else _("Не заполнено")


class WorksByKaleGallery(models.Model):
    title_uz = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    title_en = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    title_ru = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    text_uz = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    text_en = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    text_ru = models.TextField(default='matn kiritilmagan', null=True, blank=True)

    def __str__(self):
        return self.title_ru if self.title_ru else _("Не заполнено")

    class Meta:
        verbose_name = _("Работа в галерее kale")
        verbose_name_plural = _("Работы Кале галереи")


class WorksByKaleGalleryShots(models.Model):
    works = models.ForeignKey("basic_app.WorksByKaleGallery", on_delete=models.CASCADE)
    image = models.ImageField(_("Изображение для галереи"))

    class Meta:
        verbose_name = _("Изображение для галереи")
        verbose_name_plural = _("Изображение для галереи")


class InfoGrafika(models.Model):
    nominal_product = models.CharField(max_length=30, default='40')
    partners = models.CharField(max_length=30, default='10')
    nominal_products = models.CharField(max_length=30, default='40')
    nominal_products_last = models.CharField(max_length=30, default='40')
    text = models.TextField(default='matn kiritilmagan')

    def __str__(self):
        return self.nominal_product

    class Meta:
        verbose_name_plural = 'Infografika'


class GalleryOnlyImages(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name_plural = 'Gallery_Only_Images'


class Partners(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name_plural = 'Partners'


class Gallery_News(models.Model):
    title_uz = models.CharField(max_length=512, default='matn kiritilmagan')
    title_ru = models.CharField(max_length=512, default='matn kiritilmagan')
    title_en = models.CharField(max_length=512, default='matn kiritilmagan')
    text_uz = models.TextField(default='matn kiritilmagan')
    text_ru = models.TextField(default='matn kiritilmagan')
    text_en = models.TextField(default='matn kiritilmagan')
    img = models.ImageField(upload_to='images/')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title_ru} - {self.time.strftime('%d.%m.%Y') if self.time else 'no time set'}"

    class Meta:
        verbose_name = 'Gallery_News'
        verbose_name_plural = 'Gallery_News'


class Form(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=128, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Ismi: {self.name}\nTelefon raqami: {self.phone}\nManzil: {self.address}'

    class Meta:
        verbose_name_plural = 'Form'


class SocialNetworks(models.Model):
    instagram_link = models.URLField(max_length=512, default='link kiritilmagan', null=True, blank=True)
    facebook_link = models.URLField(max_length=512, default='link kiritilmagan', null=True, blank=True)
    telegram_link = models.URLField(max_length=512, default='link kiritilmagan', null=True, blank=True)
    youtube_link = models.URLField(max_length=512, default='link kiritilmagan', null=True, blank=True)
    whatsapp_link = models.URLField(max_length=512, default='link kiritilmagan', null=True, blank=True)
    linkedin_link = models.URLField(max_length=512, default='link kiritilmagan', null=True, blank=True)
    twitter_link = models.URLField(max_length=512, default='link kiritilmagan', null=True, blank=True)
    tiktok_link = models.URLField(max_length=512, default='link kiritilmagan', null=True, blank=True)
    pinterest_link = models.URLField(max_length=512, default='link kiritilmagan', null=True, blank=True)

    def __str__(self):
        return self.instagram_link

    class Meta:
        verbose_name_plural = 'Social_Networks'


class Location(models.Model):
    title_uz = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    title_en = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    title_ru = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    text_uz = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    text_ru = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    text_en = models.TextField(default='matn kiritilmagan', null=True, blank=True)

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name_plural = 'Location'


class UsedProductsInWorksKale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name_plural = "Использованные товары в комнате"


class WorksByKale(models.Model):
    title_uz = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    title_ru = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    title_en = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    text_uz = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    text_ru = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    text_en = models.TextField(default='matn kiritilmagan', null=True, blank=True)
    image1 = models.ImageField(upload_to='images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='images/', null=True, blank=True)
    tour_link = models.URLField(null=True, blank=True)
    long_desc_text_uz = models.TextField(null=True, blank=True)
    long_desc_text_ru = models.TextField(null=True, blank=True)
    long_desc_text_en = models.TextField(null=True, blank=True)
    used_products = models.ManyToManyField(UsedProductsInWorksKale, blank=True)

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name_plural = 'Works_By_Kale'


class ProductWorksByCompany(models.Model):
    product = models.ForeignKey("basic_app.WorksByKale", on_delete=models.CASCADE)
    image = models.ImageField(_("Изображение"))

    class Meta:
        verbose_name = _("Изображение сделанных работ")
        verbose_name_plural = _("Изображение сделанных работ")

    def __str__(self):
        return str(self.product)


class Discount(models.Model):
    name = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    phone_number = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    location = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    discount_name = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    total_cost = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"Ismi: {self.name}\n" \
               f"Telefon raqami: {self.phone_number}\n" \
               f"Manzili: {self.location}\n" \
               f"Chegirma nomi: {self.discount_name}\n" \
               f"Umumiy narxi: {self.total_cost}"

    class Meta:
        verbose_name_plural = 'Discount'


class BarabanDiscount(models.Model):
    name_uz = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    name_ru = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    name_en = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Baraban_Discount'


class Orders(models.Model):
    name = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    phone_number = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    location = models.CharField(max_length=512, default='matn kiritilmagan', null=True, blank=True)
    total_cost = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"Ismi: {self.name}\n" \
               f"Telefon raqami: {self.phone_number}\n" \
               f"Manzili: {self.location}\n" \
               f"Umumiy narxi: {self.total_cost}"


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.room)


class Header_Carusel(models.Model):
    nomi_uz = models.CharField(max_length=200, default='none', null=True, blank=True)
    nomi_en = models.CharField(max_length=200, default='none', null=True, blank=True)
    nomi_ru = models.CharField(max_length=200, default='none', null=True, blank=True)
    text_uz = models.TextField(default='none', null=True, blank=True)
    text_ru = models.TextField(default='none', null=True, blank=True)
    text_en = models.TextField(default='none', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.nomi_ru

    def image_url(self):
        urls = []
        for img in self.image.all():
            urls.append(img.url())
        return urls

    class Meta:
        verbose_name_plural = 'header_carusel'


class TopProductCategory(models.Model):
    name_ru = models.CharField(_("Название категории ru"), max_length=100)
    name_uz = models.CharField(_("Kategoriya nomi uz"), max_length=100, null=True, blank=True)
    name_en = models.CharField(_("Product category en"), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Топ Бренд")
        verbose_name_plural = _("Топ Бренды")

    def __str__(self):
        return self.name_ru


class TopProduct(models.Model):
    title_ru = models.CharField(_("Наименование товара ru"), max_length=255, null=True, blank=True)
    title_uz = models.CharField(_("Tovar nomi uz"), max_length=255, null=True, blank=True)
    title_en = models.CharField(_("Product name en"), max_length=255, null=True, blank=True)
    code = models.CharField(_("Код товара"), max_length=50, null=True, blank=True)
    unit = models.CharField(_("Единица измерения"), choices=ProductUnitChoices.choices,
                            default=ProductUnitChoices.PIECE, max_length=10)
    brand = models.CharField(_("Торговая марка"), max_length=50, null=True, blank=True)
    proportions = models.CharField(_("Размеры"), max_length=30)
    description_ru = models.TextField(_("Описание ru"), null=True, blank=True)
    description_uz = models.TextField(_("Tavsif uz"), null=True, blank=True)
    description_en = models.TextField(_("Description en"), null=True, blank=True)
    manufacturer = models.CharField(_("Производитель"), max_length=20, null=True, blank=True)
    category = models.ForeignKey("basic_app.TopProductCategory", on_delete=models.PROTECT, null=True, blank=True)
    rest_count = models.FloatField(_("Остаток товара"), default=0)
    is_float = models.BooleanField(_("Остаток является нецелым"), default=False)
    price = models.IntegerField(_("Цена"), default=0)
    is_deleted = models.BooleanField(_("Удален ли товар"), default=False)

    class Meta:
        verbose_name = _("Топ Товар")
        verbose_name_plural = _("Топ Товары")

    def __str__(self):
        return self.title_ru if self.title_ru else _("Не заполнено")


class TopProductShots(models.Model):
    product = models.ForeignKey("basic_app.TopProduct", on_delete=models.CASCADE)
    image = models.ImageField(_("Изображение"))

    class Meta:
        verbose_name = _("Топ Изображение товара")
        verbose_name_plural = _("Топ Изображения товаров")


class ModelObjects(models.Model):
    name_uz = models.TextField()
    name_ru = models.TextField()
    name_en = models.TextField()

    def __str__(self):
        return self.name_ru


class MyObjects(models.Model):
    key = models.TextField()
    object = models.ForeignKey(ModelObjects, on_delete=models.CASCADE)

    def __str__(self):
        return self.key


# from django.db import models
# from django.conf import settings
# from django.db import models
# from django.contrib.auth.models import User
#
#
# # Create your models here.
#
# class Conversation(models.Model):
#     initiator = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_starter"
#     )
#     receiver = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_participant"
#     )
#     start_time = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.initiator} to {self.receiver}"
#
#
# class Message(models.Model):
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
#                                null=True, related_name='message_sender')
#     text = models.CharField(max_length=200, blank=True)
#     attachment = models.FileField(blank=True)
#     conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, )
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ('-timestamp',)
#
#     def __str__(self):
#         return f"{self.sender} to {self.conversation_id}"
#
#
# class Conversation_NEW(models.Model):
#     room_name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return f'Room: {self.room_name} ID:{str(self.id)}'
#
#
# class Message_NEW(models.Model):
#     conversation = models.ForeignKey(Conversation_NEW, on_delete=models.CASCADE)
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.message
