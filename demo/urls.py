from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import store.views
from store.api_views import ProductList, ProductCreate, \
    ProductRetrieveUpdateDestroy, ProductStats

urlpatterns = [
                  path('api/v1/products/', ProductList.as_view()),
                  path('api/v1/products/new/', ProductCreate.as_view()),
                  path('api/v1/products/<int:id>/',
                       ProductRetrieveUpdateDestroy.as_view()),
                  path('api/v1/products/<int:id>/stats/',
                       ProductStats.as_view()),

                  path('admin/', admin.site.urls),
                  path('products/<int:id>/', store.views.show,
                       name='show-product'),
                  path('cart/', store.views.cart, name='shopping-cart'),
                  path('', store.views.index, name='list-products'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


