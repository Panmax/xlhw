# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Goods(models.Model):
    GOODSTYPE_IN_CHOICES = (
        (0, '手机'),
        (1, '配件'),
        (3, '其它')
    )
    name = models.CharField(max_length=15)
    price = models.FloatField()
    goods_type = models.IntegerField(choices=GOODSTYPE_IN_CHOICES)  # 1手机 2配件 3其它
    unsalable = models.BooleanField(default=False)
    add_people = models.ForeignKey(User)
    update_date = models.DateField(auto_now_add=True)
    recent_sell = models.DateField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=10)
    principal = models.ForeignKey(User)  # 负责人

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class GoodsShop(models.Model):
    goods = models.ForeignKey(Goods)
    shop = models.ForeignKey(Shop)
    remain = models.IntegerField()  # 剩余
    last_updater = models.ForeignKey(User)
    last_update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s--%s" % (self.shop, self.goods)


class SellRecord(models.Model):
    shop = models.ForeignKey(Shop)
    goods = models.ForeignKey(Goods)
    amount = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s--%s--%s" % (self.shop, self.goods, self.amount)


class GoodsRecord(models.Model):
    goods = models.ForeignKey(Goods)
    shop = models.ForeignKey(Shop)
    change_num = models.IntegerField()
    remark = models.TextField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    sell_record = models.ForeignKey(SellRecord, blank=True, null=True)
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s--%s" % (self.shop, self.goods)


class ReturnRecord(models.Model):
    TYPE_IN_CHOICES = (
        (0, '操作失误'),
        (1, '退货'),
    )
    shop = models.ForeignKey(Shop)
    goods = models.ForeignKey(Goods)
    amount = models.IntegerField()
    type = models.IntegerField(choices=TYPE_IN_CHOICES)
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s--%s--%s" % (self.shop, self.goods, self.amount)


class TransferGoods(models.Model):
    from_shop = models.ForeignKey(Shop, related_name='from_shop')
    to_shop = models.ForeignKey(Shop, related_name='to_name')
    goods = models.ForeignKey(Goods)
    change_num = models.IntegerField()
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s--%s--%s--%s" % (self.from_shop, self.to_shop, self.goods, self.change_num)


class ChangePrice(models.Model):
    goods = models.ForeignKey(Goods)
    old_price = models.FloatField()
    new_price = models.FloatField()
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.goods.name


class Backup(models.Model):
    GOODSTYPE_IN_CHOICES = (
        (0, '手机'),
        (1, '配件'),
        (3, '其它')
    )
    goods_name = models.CharField(max_length=15)
    goods_type = models.IntegerField(choices=GOODSTYPE_IN_CHOICES)
    dadian_count = models.IntegerField()
    guoaodian_count = models.IntegerField()
    hongweidian_count = models.IntegerField()
    is_lastet = models.BooleanField(default=True)
    save_datetime = models.DateTimeField(auto_now_add=True)

class ShopPhoneColor(models.Model):
    goodsshop = models.ForeignKey(GoodsShop)
    color = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.color
