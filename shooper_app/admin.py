from django.contrib import admin
from .models import*
# Register your models here.

# Contact details
class contactDetail(admin.ModelAdmin):
    list_display=['name','email' ,'subject' ,'message' ,'time']
admin.site.register(Contact,contactDetail)

# Registration Details
class registrationDetail(admin.ModelAdmin):
    list_display=['name' ,'email' ,'password' ,'time', 'otp']
admin.site.register(User,registrationDetail)

class main_category_show(admin.ModelAdmin):
    list_display=['name' ]
class sub_category_show(admin.ModelAdmin):
    list_display=['name']    
admin.site.register(main_category,main_category_show)
admin.site.register(sub_category,sub_category_show)
admin.site.register(product)
admin.site.register(price_filter)
admin.site.register(add_cart)
admin.site.register(address)
admin.site.register(order1)
admin.site.register(coupon)
admin.site.register(review_details)
admin.site.register(size_filter)
