from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from basic_app import views
from basic_app.views import UserViewSet, ProductsViewSet, ProductCategoryViewSet, AboutViewSet, BestSerllerViewSet, \
    WorksByKaleGalleryrViewSet, AllProductsViewSet, InfografikaViewSet, \
    GalleryOnlyImagesViewSet, PartnersViewSet, Gallery_NewsViewSet, FormViewSet, \
    SocialNetworksViewSet, LocationViewSet, WorksByKaleViewSet, DiscountViewSet, ProductFilterViewSet, \
    ProductListByCategory, BarabanDiscountViewSet, OrdersViewSet, HeaderViewSet, TopProductsViewSet, \
    TopProductCategoryViewSet, ChatRoomViewSet, ChatMessageViewSet, MyObjectsListView
from conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register('products', ProductsViewSet)
router.register('category', ProductCategoryViewSet)
router.register('about', AboutViewSet)
router.register('best_seller', BestSerllerViewSet)
router.register('works_kale_gallery', WorksByKaleGalleryrViewSet)
router.register('all_products', AllProductsViewSet)
router.register('infografika', InfografikaViewSet)
router.register('gallery_only_images', GalleryOnlyImagesViewSet)
router.register('partners', PartnersViewSet)
router.register('gallery_news', Gallery_NewsViewSet)
router.register('form', FormViewSet)
router.register('social_networks', SocialNetworksViewSet)
router.register('location', LocationViewSet)
router.register('works_by_kale', WorksByKaleViewSet)
router.register('discount', DiscountViewSet)
router.register('filter', ProductFilterViewSet, basename='max')
# router.register('filter/min', ProductFilterViewSet, basename='min')
router.register('all_data', ProductListByCategory, basename='all_data')
router.register('baraban', BarabanDiscountViewSet, basename='data')
router.register('orders', OrdersViewSet, basename='datas')
router.register('header', HeaderViewSet, basename='header')
router.register('top_products', TopProductsViewSet, basename='topproduct')
router.register('top_products_category', TopProductCategoryViewSet, basename='topproductcategory')
router.register('chat_room', ChatRoomViewSet, basename='room')
router.register('chat_message', ChatMessageViewSet, basename='message')
router.register('objects', MyObjectsListView, basename='obejcts')

app_name = "api"
urlpatterns = router.urls

# router = routers.DefaultRouter()
router.register(r'objects', views.MyObjectsListView, basename='objects')

urlpatterns = [
]

urlpatterns += router.urls
