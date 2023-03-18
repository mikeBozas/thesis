from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


# Register your models here.
from .models import Insurer, Customer, Insurance


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Insurer


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('first_name', 'last_name', 'address', 'age', 'AFM', 'employee_externalPartner',)}),
    # )


admin.site.register(Insurer, MyUserAdmin)
admin.site.register(Customer)
admin.site.register(Insurance)

admin.site.unregister(Group)