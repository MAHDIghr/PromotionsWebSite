from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('FAQ', views.faq, name='faq'),
    path('About', views.about, name='about'),
    path('Contact', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('<str:seller_site>/', views.products_by_seller, name='products_by_seller'),
    path('products/with-promo-code/', views.products_with_promo_code, name='products_with_promo_code'),
    path('products/without-promo-code/', views.products_without_promo_code, name='products_without_promo_code'),
    path('products/best-promo/', views.products_with_bestPromo, name='products_with_bestPromo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
