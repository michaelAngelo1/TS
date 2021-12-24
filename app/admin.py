from django.contrib import admin
from django.forms import *
from .models import Promo, Telemarketing, Akun,Player, Deposit, Withdraw, TransferAntarAkun, Bonus
from django.db import models

admin.site.register(Promo)
admin.site.register(Telemarketing)
admin.site.register(Player)

class AkunAdmin(admin.ModelAdmin):
    fields = ['NamaAkun', 'Saldo', 'Keterangan']

    formfield_overrides = {models.IntegerField: {'widget': TextInput(attrs={'size': '20'})}}
admin.site.register(Akun, AkunAdmin)


class DepositAdmin(admin.ModelAdmin):
    fields = ['Player', 'Bank', 'Nominal', 'Referensi', 'Promo', 'Charge']
    list_display = ("Player", "Bank", "Nominal", "Referensi", "Promo", "Charge", "CreateBy", "Operator")
    list_filter = ("Player", "Nominal")

    # Delete Symbol
    formfield_overrides = {
        models.IntegerField : {'widget': NumberInput(attrs={'size':'50'})}
    }
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'Player' or db_field.name=='Bank' or db_field.name=='Promo':
            #formfield.widget.can_add_related = False
            #formfield.widget.can_change_related = False
            formfield.widget.can_delete_related = False
        return formfield

    ordering = ("Player",)

    # Get createby and operator username
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'CreateBy', None) is None:
            obj.CreateBy = request.user.username
            obj.Operator = request.user.username
        elif getattr(obj, 'Operator', None) != request.user.username:
            obj.Operator = request.user.username
        obj.save()

    def get_queryset(self, request):
        qs = super(DepositAdmin, self).get_queryset(request)
        return qs.filter(CreateBy=request.user.username)
    # Restrict anyone to see what's created
   # def Player(self, obj):
   #    return f'{obj.Player} -> {obj.Nominal:,}'
   # def get_queryset(self):
   #    return super().get_queryset().filter(CreateBy=request.user.username)



admin.site.register(Deposit, DepositAdmin)

class WithdrawAdmin(admin.ModelAdmin):
    fields = ['Player', 'Bank', 'Nominal', 'Referensi', 'Promo', 'Charge']
admin.site.register(Withdraw,WithdrawAdmin)

class TransferAdmin(admin.ModelAdmin):
    fields = ['AkunAsal', 'Nominal', 'Charge', 'AkunTujuan']
admin.site.register(TransferAntarAkun, TransferAdmin)

class BonusAdmin(admin.ModelAdmin):
    fields = ['Player', 'Nominal', 'Promo', 'Keterangan']
admin.site.register(Bonus, BonusAdmin)


