from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (Cart, Contact, Customer, CustomUser, Deal, Order, Product,
                     ProductInCart, Seller, SellerAdditional, CustomerAdditional)

admin.site.register(Product)
admin.site.register(ProductInCart)
# admin.site.register(Cart)
admin.site.register(Order)
# admin.site.register(Deal)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "type")
    # list_display = ("email", "is_staff", "is_active", "is_customer", "is_seller")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "type")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)


# customize admin
class CartInline(admin.TabularInline):
    model = Cart  # for onetoone ,foreignkey


class DealInline(admin.TabularInline):
    model = Deal.user.through  # for manytomany field


# # DEFAULT USER MODEL
# class UserAdmin(UserAdmin):
#     model = User
#     list_display = ('username', 'get_cart', 'is_staff', 'is_active')
#     list_filter = ('username', 'is_staff', 'is_active', 'is_superuser')
#     fieldsets = (
#         ('User Details', {'fields': ('username', 'password')}),
#         ('Permissions', {'fields': ('is_staff', ('is_active', 'is_superuser'),)}),
#         ('Important Date', {'fields': ('last_login', 'date_joined')}),
#         ('Advanced options', {
#             'classes': ('collapse',),
#             'fields': ('groups', 'user_permissions',)
#         }),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),  # class for css
#             'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups',)}
#          # fields shown on create a user
#          ),
#     )
#     inlines = [CartInline, DealInline]
#
#     def get_cart(self, obj):
#         return obj.cart
#
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


# customize admin
class ProductInCartline(admin.TabularInline):
    model = ProductInCart  # for onetoone ,foreignkey


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('staff', 'user', 'created_on')  # here user__is_staffwill not work
    list_filter = ('user', 'created_on')
    fieldsets = (
        ('Cart Detail', {'fields': ('user', 'created_on',)}),
    )
    inlines = (
        ProductInCartline,
    )

    def staff(self, obj):
        return obj.user.is_staff

    staff.admin_order_field = 'user__is_staff'  # allow column order sorting
    staff.short_description = 'Staff User'  # rename column head

    # filtering on the side
    list_filter = ['user__is_staff',
                   'created_on']  # with direct foreignkey (user) no error , but not shown in filters , with function errors.
    search_fields = ['user__username']  # with direct foreignkey (user) no error but filtering not possible directly


class DealAdmin(admin.ModelAdmin):
    inlines = [DealInline]
    exclude = ('user',)

class SellerAdditionalInline(admin.TabularInline):
    model = SellerAdditional


class SellerAdmin(admin.ModelAdmin):
    inlines = (
        SellerAdditionalInline,
    )

admin.site.register(Deal, DealAdmin)
# admin.site.register(UserType)
admin.site.register(Customer)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Contact)
admin.site.register(CustomerAdditional)
