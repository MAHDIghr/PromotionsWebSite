from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('FAQ', views.faq, name='faq'),
    path('About', views.about, name='about'),
    path('Contact', views.contact, name='contact'),
    path('Contact/message-envoyé', views.contact_after_submit, name='contact_after_submit'),
    path('recherche/', views.search, name='search'),
    path('increment-click/<slug:slug>/', views.increment_click_and_redirect, name='increment_click'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('categorie/<str:category_name>/', views.category_products, name='category_products'),
    path('vendeur/<str:seller_site>/', views.products_by_seller, name='products_by_seller'),
    path('produits/avec-code-promo/', views.products_with_promo_code, name='products_with_promo_code'),
    path('produits/sans-code-promo/', views.products_without_promo_code, name='products_without_promo_code'),
    path('produits/meillieurs-promo/', views.products_with_bestPromo, name='products_with_bestPromo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
