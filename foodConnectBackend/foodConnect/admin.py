from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
admin.site.register(RestaurantTrail)
admin.site.register(Reviews)
admin.site.register(Friends)
admin.site.register(ReviewImages)

