from django.contrib import admin

from basic_app.models import Product, ProductShots, ProductCategory, ProductUpdateLog, About, BestSellerProducts, \
    WorksByKaleGallery, WorksByKaleGalleryShots, InfoGrafika, GalleryOnlyImages, Partners, Gallery_News, Form, \
    SocialNetworks, Location, WorksByKale, Discount, BarabanDiscount, Orders, Header_Carusel, TopProduct, \
    TopProductCategory, TopProductShots, ChatRoom, ChatMessage, MyObjects, ModelObjects, ProductWorksByCompany, \
    UsedProductsInWorksKale


class ProductShotsInline(admin.TabularInline):
    model = ProductShots
    extra = 0


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductShotsInline]
    list_display = ["title_ru", "unit", "category"]
    raw_id_fields = ["category"]
    search_fields = ['title_ru', 'id']
    # list_select_related = ["category"]
    # list_filter = ["category"]


@admin.register(ProductShots)
class ProductShotsAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']
    search_fields = ['id', 'image', 'product']

@admin.register(ProductUpdateLog)
class ProductUpdateLogAdmin(admin.ModelAdmin):
    pass


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    pass


@admin.register(BestSellerProducts)
class BestSellerProductsAdmin(admin.ModelAdmin):
    pass


@admin.register(WorksByKaleGallery)
class WorksByKaleGalleryAdmin(admin.ModelAdmin):
    pass


@admin.register(WorksByKaleGalleryShots)
class WorksByKaleGalleryShotsAdmin(admin.ModelAdmin):
    pass


@admin.register(InfoGrafika)
class InfoGrafikaAdmin(admin.ModelAdmin):
    pass


# @admin.register(GalleryOnlyImages)
# class GalleryOnlyImagesAdmin(admin.ModelAdmin):
#     pass


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    pass


@admin.register(Gallery_News)
class Gallery_NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialNetworks)
class SocialNetworksAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


class ProductWorksByCompanyInline(admin.TabularInline):
    model = ProductWorksByCompany
    extra = 0


@admin.register(WorksByKale)
class WorksByKaleAdmin(admin.ModelAdmin):
    inlines = [ProductWorksByCompanyInline]


@admin.register(UsedProductsInWorksKale)
class UsedProductsInWorksKaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']
    search_fields = ['product__title_ru', 'product__title_uz', 'product__title_en']


@admin.register(ProductWorksByCompany)
class ProductWorksByCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(BarabanDiscount)
class BarabanDiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    pass


@admin.register(Header_Carusel)
class Header_CaruselAdmin(admin.ModelAdmin):
    pass


# class TopProductShotsInline(admin.TabularInline):
#     model = TopProductShots
#     extra = 0


# @admin.register(TopProduct)
# class TopProductAdmin(admin.ModelAdmin):
#     inlines = [TopProductShotsInline]
#     list_display = ["title_ru", "unit", "category"]
#     raw_id_fields = ["category"]


# @admin.register(TopProductCategory)
# class TopProductCategoryAdmin(admin.ModelAdmin):
#     pass


# @admin.register(TopProductShots)
# class TopProductShotsAdmin(admin.ModelAdmin):
#     pass


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(MyObjects)
class MyModelJsonAdmin(admin.ModelAdmin):
    pass


@admin.register(ModelObjects)
class MyModelJsonAdmin(admin.ModelAdmin):
    pass
