from django.contrib import admin

from .models import *

admin.site.register([Admin,Customer,Order,Product,Category,Cart,CartProduct,ProductImage])