from django.contrib import admin
from .models import Store, Customer, User

# Register your models here.


class RegisterStore(admin.ModelAdmin):
    list_display = ("store_name", "address")
    search_fields = ("store_name", "company_name" "address")


admin.site.register(Store, RegisterStore)


class RegisterCustomer(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


admin.site.register(Customer, RegisterCustomer)


class RegisterUser(admin.ModelAdmin):
    list_display = ("email",)
    search_fields = ("email",)


admin.site.register(User, RegisterUser)
