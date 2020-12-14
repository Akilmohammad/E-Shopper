from django.contrib import admin
from . models import User,CONTACT, WOMEN_CLOTH, MEN_CLOTH,CHECKOUT,Transaction, WOMEN_ACCESSORIES, MEN_ACCESSORIES, WOMEN_FOOTWEAR, MEN_FOOTWEAR,WISHLIST,CART
# Register your models here.
admin.site.register(User)
admin.site.register(CONTACT)
admin.site.register(WOMEN_CLOTH)
admin.site.register(MEN_CLOTH)
admin.site.register(WOMEN_ACCESSORIES)
admin.site.register(MEN_ACCESSORIES)
admin.site.register(WOMEN_FOOTWEAR)
admin.site.register(MEN_FOOTWEAR)
admin.site.register(WISHLIST)
admin.site.register(CART)
admin.site.register(CHECKOUT)
admin.site.register(Transaction)