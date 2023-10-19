from django.contrib.auth import get_user_model
from django.db.models import Q, Max, Min
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import filters
from basic_app.models import Product, ProductCategory, ProductShots, About, BestSellerProducts, WorksByKaleGallery, \
    InfoGrafika, GalleryOnlyImages, Partners, Gallery_News, Form, SocialNetworks, Location, WorksByKale, Discount, \
    BarabanDiscount, Orders, Header_Carusel, TopProduct, TopProductCategory, TopProductShots, ChatRoom, ChatMessage, \
    MyObjects, ModelObjects
from basic_app.serializers import ProductCategorySerializer, ProductShotsSerializer, ProductSerializer, \
    AboutSerializer, BestSellerSerializer, WorksByKaleGallerySerializer, InfografikaSerializer, \
    GalleryOnlyImagesSerializer, PartnersSerializer, Gallery_NewsSerializer, FormSerializer, SocialNetworksSerializer, \
    LocationSerializer, WorksByKaleSerializer, DiscountSerializer, BarabanDiscountSerializer, OrdersSerializer, \
    HeaderCaruselSerializer, TopProductSerializer, TopProductCategorySerializer, TopProductShotsSerializer, \
    ChatRoomSerializer, ChatMessageSerializer, MyObjectsSerializer, ModelObjectsSerializer
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 50


User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ProductsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Product.objects.exclude(category__name_ru='Шкаф').filter(productshots__isnull=False, price__gt=0,
                                                                        rest_count__gt=0).distinct().order_by('-id')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title_ru', 'title_uz',
                     'title_en', 'category__name_ru', 'category__name_en', 'category__name_uz']
    ordering_fields = ['price', 'title_ru', 'title_uz', 'title_en']


class AllProductsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    # queryset = Product.objects.exclude(rest_count__gt=0, category__name_ru='Шкаф', price__gt=0).all()
    queryset = Product.objects.exclude(category__name_ru='Шкаф').filter(productshots__isnull=False, price__gt=0,
                                                                        rest_count__gt=0).distinct().order_by('-id')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title_ru', 'title_uz', 'title_en', 'category__name_ru', 'category__name_uz', 'category__name_en']


class ProductCategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = ProductCategory.objects.exclude(name_ru='Шкаф').filter(product__isnull=False).distinct()
    serializer_class = ProductCategorySerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name_ru', 'name_en',
                     'name_uz']

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(product__isnull=False).distinct()
        return super().list(request, *args, **kwargs)


class ProductShotsSerializerViewSet(ListModelMixin, GenericViewSet):
    queryset = ProductShots.objects.all()
    serializer_class = ProductShotsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product']
    search_fields = ['product__title_ru', 'product__title_ru',
                     'product__title_ru']


class AboutViewSet(ListModelMixin, GenericViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    pagination_class = None


class BestSerllerViewSet(ListModelMixin, GenericViewSet):
    queryset = BestSellerProducts.objects.all()
    serializer_class = BestSellerSerializer
    pagination_class = None


class WorksByKaleGalleryrViewSet(ListModelMixin, GenericViewSet):
    queryset = WorksByKaleGallery.objects.all()
    serializer_class = WorksByKaleGallerySerializer
    pagination_class = None


class InfografikaViewSet(ListModelMixin, GenericViewSet):
    queryset = InfoGrafika.objects.all()
    serializer_class = InfografikaSerializer
    pagination_class = None


class GalleryOnlyImagesViewSet(ListModelMixin, GenericViewSet):
    queryset = GalleryOnlyImages.objects.all()
    serializer_class = GalleryOnlyImagesSerializer
    pagination_class = None


class ProductFilterViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    ordering_fields = ['price']
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['category__name_ru', 'category__name_en', 'category__name_uz']

    def get_queryset(self):
        print(vars(self), 'bu self yangi')
        print(vars(self.request), 'bu self request')
        queryset = Product.objects.exclude(category__name_ru='Шкаф').filter(productshots__isnull=False, price__gt=0,
                                                                            rest_count__gt=0).distinct().order_by('-id')
        if self.action == 'max':
            queryset = self.filter_queryset_by_category(queryset)
            queryset = queryset.filter(price__gte=2000000)
        elif self.action == 'min':
            queryset = self.filter_queryset_by_category(queryset)
            queryset = queryset.filter(Q(price__lte=2000000) | Q(price=None))
        return queryset

    def filter_queryset_by_category(self, queryset):
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    @action(detail=False, methods=['get'])
    def max(self, request):
        return self.list(request)

    @action(detail=False, methods=['get'])
    def min(self, request):
        return self.list(request)


class ProductsByCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        price_filter = kwargs.get('price')
        products = Product.objects.all()
        if price_filter == 'max':
            product = products.filter(price__gte='2000000')
        elif price_filter == 'min':
            product = products.filter(price__lt='2000000')
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


class PartnersViewSet(ListModelMixin, GenericViewSet):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializer
    pagination_class = None


class Gallery_NewsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Gallery_News.objects.all()
    serializer_class = Gallery_NewsSerializer
    pagination_class = None


class FormViewSet(CreateModelMixin, GenericViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    pagination_class = None


class SocialNetworksViewSet(ListModelMixin, GenericViewSet):
    queryset = SocialNetworks.objects.all()
    serializer_class = SocialNetworksSerializer
    pagination_class = None


class LocationViewSet(ListModelMixin, GenericViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = None


class WorksByKaleViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = WorksByKale.objects.all()
    serializer_class = WorksByKaleSerializer
    pagination_class = None


class DiscountViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    pagination_class = None


class CustomPaginationNew(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductListByCategory(ListModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    pagination_class = CustomPaginationNew
    queryset = Product.objects.none()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category']
    ordering_fields = ['price', 'name_uz', 'name_ru', 'name_en']
    search_fields = ['category__name_ru', 'category__name_uz', 'category__name_en']

    def get_queryset(self):
        categories = ProductCategory.objects.all()
        q_objects = Q()
        for category in categories:
            q_objects |= Q(category__name_ru__icontains=self.request.query_params.get('search', ''))
            q_objects |= Q(category__name_uz__icontains=self.request.query_params.get('search', ''))
            q_objects |= Q(category__name_en__icontains=self.request.query_params.get('search', ''))
        queryset = Product.objects.filter(q_objects).order_by('-rest_count')[:5]
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class BarabanDiscountViewSet(ListModelMixin, GenericViewSet):
    queryset = BarabanDiscount.objects.all()
    serializer_class = BarabanDiscountSerializer
    pagination_class = None


class OrdersViewSet(CreateModelMixin, GenericViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    pagination_class = None


class HeaderViewSet(ListModelMixin, GenericViewSet):
    queryset = Header_Carusel.objects.all()
    serializer_class = HeaderCaruselSerializer
    pagination_class = None


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'name_uz', 'name_ru', 'name_en']

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort_by', None)
        if sort_by:
            if sort_by == 'name':
                queryset = queryset.order_by('name_ru')
            elif sort_by == 'price':
                queryset = queryset.order_by('price')
        return queryset


class TopProductsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Product.objects.exclude(category__name_ru='Шкаф').filter(productshots__isnull=False, price__gt=0,
                                                                        rest_count__gt=0,
                                                                        top_product=True).distinct().order_by('-id')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title_ru', 'title_uz', 'price',
                     'title_en', 'category__name_ru', 'category__name_en', 'category__name_uz']
    ordering_fields = ['price', 'title_ru', 'title_uz', 'title_en']


class TopProductCategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = ProductCategory.objects.exclude(name_ru='Шкаф').filter(product__isnull=False,
                                                                      product__top_product=True).distinct()
    serializer_class = ProductCategorySerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name_ru', 'name_en',
                     'name_uz']


class TopProductShotsSerializerViewSet(ListModelMixin, GenericViewSet):
    queryset = TopProductShots.objects.all()
    serializer_class = TopProductShotsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product']
    search_fields = ['product__title_ru', 'product__title_ru',
                     'product__title_ru']


class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class ChatMessageViewSet(ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['room']
    # search_fields = ['product__title_ru', 'product__title_ru',
    #                  'product__title_ru']


class ModelObjectList(generics.ListCreateAPIView):
    queryset = ModelObjects.objects.all()
    serializer_class = ModelObjectsSerializer


class ModelObjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ModelObjects.objects.all()
    serializer_class = ModelObjectsSerializer


class MyObjectsListView(ListModelMixin, GenericViewSet):
    serializer_class = ModelObjectsSerializer
    queryset = MyObjects.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = {}
        for obj in queryset:
            key_name = f"{obj.key}"
            model_object = obj.object
            data[key_name] = {
                'name_uz': model_object.name_uz,
                'name_ru': model_object.name_ru,
                'name_en': model_object.name_en,
            }
        return Response(data)


class MyObjectsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyObjects.objects.all()
    serializer_class = MyObjectsSerializer
