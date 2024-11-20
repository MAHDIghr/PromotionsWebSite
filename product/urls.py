from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('FAQ', views.faq, name='faq'),
    path('About', views.about, name='about'),
    path('Contact', views.contact, name='contact'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('<str:seller_site>/', views.products_by_seller, name='products_by_seller'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
