from django.contrib import admin

# Register your models here.
from models import GoodsShop, Goods, Shop, GoodsRecord, ChangePrice, Backup, ReturnRecord, SellRecord

admin.site.register(Shop)

admin.site.register(GoodsShop)
admin.site.register(GoodsRecord)
admin.site.register(ChangePrice)
admin.site.register(ReturnRecord)
admin.site.register(SellRecord)


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'update_date', 'recent_sell', 'is_delete')


class BackupAdmin(admin.ModelAdmin):
    list_display = ('goods_name', 'goods_type', 'save_datetime')


admin.site.register(Goods, GoodsAdmin)
admin.site.register(Backup, BackupAdmin)