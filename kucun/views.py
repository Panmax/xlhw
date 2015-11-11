# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from models import Goods, Shop, GoodsShop, GoodsRecord, TransferGoods, ChangePrice, Backup, ReturnRecord, \
    SellRecord, ShopPhoneColor


@login_required(login_url='/kucun/login')
def all_phone(request):
    phones = Goods.objects.filter(goods_type=0, is_delete=False).order_by('name')

    datas = []
    amount = 0
    for phone in phones:
        guoao = GoodsShop.objects.get(goods=phone, shop__name='国奥店')
        dadian = GoodsShop.objects.get(goods=phone, shop__name='大店')
        hongwei = GoodsShop.objects.get(goods=phone, shop__name='红卫店')
        all_num = guoao.remain + dadian.remain + hongwei.remain
        today = datetime.date.today()
        if phone.recent_sell == today - datetime.timedelta(days=1):
            phone.show_color = True
        if phone.update_date == today:
            phone.updated = True

        m = {'goods': phone, 'guoao': guoao, 'dadian': dadian, 'hongwei': hongwei, 'all_num': all_num}
        datas.append(m)
        amount += all_num

    shang = len(phones) / 3
    yu = len(phones) % 3
    if yu != 0:
        shang += 1

    return render_to_response('all_phone.html',
                              {'request': request, 'data1': datas[:shang], 'data2': datas[shang:shang * 2],
                               'data3': datas[shang * 2:], 'title': '总库存：手机', 'header': '总库存：手机', 'amount': amount})


@login_required(login_url='/kucun/login')
def all_peijian(request):
    peijians = Goods.objects.filter(goods_type=1, is_delete=False).order_by('name')

    datas = []
    amount = 0
    for peijian in peijians:
        guoao = GoodsShop.objects.get(goods=peijian, shop__name='国奥店')
        dadian = GoodsShop.objects.get(goods=peijian, shop__name='大店')
        hongwei = GoodsShop.objects.get(goods=peijian, shop__name='红卫店')
        all_num = guoao.remain + dadian.remain + hongwei.remain
        today = datetime.date.today()
        if peijian.recent_sell == today - datetime.timedelta(days=1):
            peijian.show_color = True
        if peijian.update_date == today:
            peijian.updated = True

        m = {'goods': peijian, 'guoao': guoao, 'dadian': dadian, 'hongwei': hongwei, 'all_num': all_num}
        datas.append(m)
        amount += all_num
    shang = len(peijians) / 3
    yu = len(peijians) % 3
    if yu != 0:
        shang += 1

    return render_to_response('all_phone.html',
                              {'request': request, 'data1': datas[:shang], 'data2': datas[shang:shang * 2],
                               'data3': datas[shang * 2:], 'title': '总库存：配件', 'header': '总库存：配件', 'amount': amount})


def delete_goods(request):
    if request.method == "GET":
        goods = Goods.objects.filter(is_delete=False).order_by('name')
        for good in goods:
            count = 0
            goods_shops = GoodsShop.objects.filter(goods=good)
            for shop in goods_shops:
                count += shop.remain
            good.count = count
        shang = len(goods) / 3
        yu = len(goods) % 3
        if yu != 0:
            shang += 1
        return render_to_response('delete_goods.html',
                                  {'request': request, 'data1': goods[:shang], 'data2': goods[shang:shang * 2],
                                   'data3': goods[shang * 2:], 'title': '删除', 'header': '删除'})
    elif request.method == 'POST':
        goods_id = request.POST['goods_id']
        goods = Goods.objects.get(id=goods_id)
        goods.is_delete = True
        goods.save()
        return HttpResponse("success")


@login_required(login_url='/kucun/login')
def hongwei_phone(request):
    goodsshops = GoodsShop.objects.filter(shop__name='红卫店', goods__goods_type=0, goods__is_delete=False).order_by(
        'goods__name')
    amount = 0
    for goodsshop in goodsshops:
        amount += goodsshop.remain
    shang = len(goodsshops) / 3
    yu = len(goodsshops) % 3
    if yu != 0:
        shang += 1
    return render_to_response('shop_phone.html',
                              {'request': request, 'data1': goodsshops[:shang], 'data2': goodsshops[shang:shang * 2],
                               'data3': goodsshops[shang * 2:], 'title': '红卫店：手机', 'header': '红卫店：手机',
                               'amount': amount})


@login_required(login_url='/kucun/login')
def hongwei_peijian(request):
    goodsshops = GoodsShop.objects.filter(shop__name='红卫店', goods__goods_type=1, goods__is_delete=False).order_by(
        'goods__name')
    amount = 0
    for goodsshop in goodsshops:
        amount += goodsshop.remain
    shang = len(goodsshops) / 3
    yu = len(goodsshops) % 3
    if yu != 0:
        shang += 1
    return render_to_response('shop_phone.html',
                              {'request': request, 'data1': goodsshops[:shang], 'data2': goodsshops[shang:shang * 2],
                               'data3': goodsshops[shang * 2:], 'title': '红卫店：配件', 'header': '红卫店：配件',
                               'amount': amount})


@login_required(login_url='/kucun/login')
def dadian_phone(request):
    goodsshops = GoodsShop.objects.filter(shop__name='大店', goods__goods_type=0, goods__is_delete=False).order_by(
        'goods__name')
    amount = 0
    for goodsshop in goodsshops:
        amount += goodsshop.remain
    shang = len(goodsshops) / 3
    yu = len(goodsshops) % 3
    if yu != 0:
        shang += 1
    return render_to_response('shop_phone.html',
                              {'request': request, 'data1': goodsshops[:shang], 'data2': goodsshops[shang:shang * 2],
                               'data3': goodsshops[shang * 2:], 'title': '大店：手机', 'header': '大店：手机', 'amount': amount})


@login_required(login_url='/kucun/login')
def dadian_peijian(request):
    goodsshops = GoodsShop.objects.filter(shop__name='大店', goods__goods_type=1, goods__is_delete=False).order_by(
        'goods__name')
    amount = 0
    for goodsshop in goodsshops:
        amount += goodsshop.remain
    shang = len(goodsshops) / 3
    yu = len(goodsshops) % 3
    if yu != 0:
        shang += 1
    return render_to_response('shop_phone.html',
                              {'request': request, 'data1': goodsshops[:shang], 'data2': goodsshops[shang:shang * 2],
                               'data3': goodsshops[shang * 2:], 'title': '大店：配件', 'header': '大店：配件', 'amount': amount})


@login_required(login_url='/kucun/login')
def guoao_phone(request):
    goodsshops = GoodsShop.objects.filter(shop__name='国奥店', goods__goods_type=0, goods__is_delete=False).order_by(
        'goods__name')
    amount = 0
    for goodsshop in goodsshops:
        amount += goodsshop.remain
    shang = len(goodsshops) / 3
    yu = len(goodsshops) % 3
    if yu != 0:
        shang += 1
    return render_to_response('shop_phone.html',
                              {'request': request, 'data1': goodsshops[:shang], 'data2': goodsshops[shang:shang * 2],
                               'data3': goodsshops[shang * 2:], 'title': '国奥店：手机', 'header': '国奥店：手机',
                               'amount': amount})


@login_required(login_url='/kucun/login')
def guoao_peijian(request):
    goodsshops = GoodsShop.objects.filter(shop__name='国奥店', goods__goods_type=1, goods__is_delete=False).order_by(
        'goods__name')
    amount = 0
    for goodsshop in goodsshops:
        amount += goodsshop.remain
    shang = len(goodsshops) / 3
    yu = len(goodsshops) % 3
    if yu != 0:
        shang += 1
    return render_to_response('shop_phone.html',
                              {'request': request, 'data1': goodsshops[:shang], 'data2': goodsshops[shang:shang * 2],
                               'data3': goodsshops[shang * 2:], 'title': '国奥店：配件', 'header': '国奥店：配件',
                               'amount': amount})


@login_required(login_url='/kucun/login')
def add_goods(request):
    if request.method == 'GET':
        return render_to_response('add_goods.html', {'request': request, 'title': '添加商品', 'header': '添加商品'})
    elif request.method == 'POST':
        user = request.user
        goodsname = request.POST['goodsname']
        price = request.POST['price']
        goodstype = request.POST['goodstype']
        goods = Goods(name=goodsname, price=price, goods_type=goodstype, add_people=user)
        goods.save()
        shops = Shop.objects.all()
        for shop in shops:
            goodsshop = GoodsShop(goods=goods, shop=shop, remain=0, last_updater=user)
            goodsshop.save()
        return HttpResponseRedirect(reverse('addsuccess'))


def add_success(request):
    return render_to_response('add_success.html', {'request': request, 'title': '添加成功'})


def mylogin(request):
    if request.method == 'GET':
        return render_to_response('login.html')
    elif request.method == 'POST':
        next = request.GET.get('next', '/kucun/all/phone/')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse('账号被锁定！')
        else:
            return HttpResponseRedirect(reverse('login_fail'))


def login_fail(request):
    return render_to_response('login_fail.html', {'request': request, 'title': '登录失败'})


def mylogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('mylogin'))


@login_required(login_url='/kucun/login')
def api_remain(request):  # 进出库
    if request.method == 'GET':
        goods_id = request.GET.get('goods_id')
        shop_id = request.GET.get('shop_id')
        goodsshop = GoodsShop.objects.get(goods=Goods.objects.get(id=goods_id), shop=Shop.objects.get(id=shop_id))
        return render_to_response('modal_change.html', {'request': request, 'goodsshop': goodsshop})
    elif request.method == 'POST':
        user = request.user
        if not user:
            return HttpResponse("false")
        shop_id = request.POST['shop_id']
        goods_id = request.POST['goods_id']
        action = request.POST.get('action')
        number = request.POST.get('number')
        remark = request.POST.get('remark')
        if number is not None and (not user.is_superuser):
            return HttpResponse('stop')

        goodsshop = GoodsShop.objects.get(goods__id=goods_id, shop__id=shop_id)
        goods = Goods.objects.get(id=goods_id)
        shop = Shop.objects.get(id=shop_id)
        if action == 'sub':
            goodsshop.remain -= 1
            if goodsshop.remain < 0:
                return HttpResponse('chaoguo')
            goodsshop.save()

            # recent_record = GoodsRecord.objects.order_by('-date')[0]
            # if recent_record.shop.id == int(shop_id) and recent_record.goods.id == int(
            # goods_id) and recent_record.updater == user:
            # recent_record.change_num -= 1

            # recent_record.save()
            #
            # # 如果是0就删除
            # if recent_record.change_num == 0:
            # recent_record.delete()
            # else:
            goods_record = GoodsRecord(goods=goods, shop=shop, change_num=-1, updater=user)
            sell_record = SellRecord(shop=shop, goods=goods, amount=1, updater=user)
            sell_record.save()
            goods_record.sell_record = sell_record
            goods_record.save()
        elif action == 'add':
            goodsshop.remain += 1
            goodsshop.save()

            # recent_record = GoodsRecord.objects.order_by('-date')[0]
            # if recent_record.shop.id == int(shop_id) and recent_record.goods.id == int(
            # goods_id) and recent_record.updater == user:
            # recent_record.change_num += 1
            # recent_record.save()
            #
            # # 如果是0就删除
            # if recent_record.change_num == 0:
            # recent_record.delete()
            # else:
            goods_record = GoodsRecord(goods=goods, shop=shop, change_num=1, updater=user)
            goods_record.save()
        elif number:
            goodsshop.remain += int(number)
            if goodsshop.remain < 0:
                return HttpResponse('chaoguo')
            goodsshop.save()

            recent_record = GoodsRecord.objects.order_by('-date')[0]
            # if recent_record.shop.id == int(shop_id) and recent_record.goods.id == int(
            # goods_id) and recent_record.updater == user:
            # recent_record.change_num += int(number)
            # recent_record.save()
            #
            # # 如果是0就删除
            # if recent_record.change_num == 0:
            # recent_record.delete()
            # else:
            if number < 0:
                sell_record = SellRecord(shop=shop, goods=goods, amount=number, updater=user)
                sell_record.save()
                goods_record = GoodsRecord(goods=goods, shop=shop, change_num=number, updater=user, remark=remark)
                goods_record.sell_record = sell_record
                goods_record.save()
            else:
                goods_record = GoodsRecord(goods=goods, shop=shop, change_num=number, updater=user, remark=remark)
                goods_record.save()

        goods.recent_sell = datetime.date.today()
        goods.save()

        return HttpResponse(goodsshop.remain)


@login_required(login_url='/kucun/login')
def api_diaoku(request):
    if request.method == 'GET':
        goods_id = request.GET.get('goods_id')
        shop_id = request.GET.get('shop_id')
        goodsshop = GoodsShop.objects.get(goods=Goods.objects.get(id=goods_id), shop=Shop.objects.get(id=shop_id))
        return render_to_response('modal_diaoku.html', {'request': request, 'goodsshop': goodsshop})
    elif request.method == 'POST':
        user = request.user
        if not user:
            return HttpResponse("false")
        from_shop_id = request.POST['from_shop_id']
        to_shop_name = request.POST['to_shop_name']
        goods_id = request.POST['goods_id']
        number = int(request.POST['number'])

        goods = Goods.objects.get(id=goods_id)
        from_shop = Shop.objects.get(id=from_shop_id)
        to_shop = Shop.objects.get(name=to_shop_name)
        if from_shop == to_shop:
            return HttpResponse('same')

        from_goodsshop = GoodsShop.objects.get(shop=from_shop, goods=goods)
        to_goodsshop = GoodsShop.objects.get(shop=to_shop, goods=goods)

        if from_goodsshop.remain < number:
            return HttpResponse('chaoguo')
        else:
            from_goodsshop.remain -= number
            from_goodsshop.save()
            to_goodsshop.remain += number
            to_goodsshop.save()
            diaoku = TransferGoods(from_shop=from_shop, to_shop=to_shop, goods=goods, change_num=number, updater=user)
            diaoku.save()

            return HttpResponse(from_goodsshop.remain)


@login_required(login_url='/kucun/login')
def api_update(request):
    if request.method == 'GET':
        goods_id = request.GET['goods_id']
        goods = Goods.objects.get(id=goods_id)
        return render_to_response('modal_update.html', {'request': request, 'goods': goods})
    elif request.method == 'POST':
        user = request.user
        if not user.is_superuser:
            return HttpResponse("stop")
        # old_goods_name = request.POST['old_goods_name']
        old_goods_price = request.POST['old_goods_price']
        name = request.POST['name']
        goods_id = request.POST['goods_id']
        price = request.POST['price']
        unsalable = request.POST['unsalable']
        if unsalable == '0':
            unsalable = False
        elif unsalable == '1':
            unsalable = True

        # if old_goods_name != name:
        # records = GoodsRecord.objects.filter(goods__name=old_goods_name)
        # if records:
        #         return HttpResponse('not_update_name')

        goods = Goods.objects.get(id=goods_id)
        goods.name = name
        goods.price = price
        goods.unsalable = unsalable
        goods.update_date = datetime.date.today()
        goods.save()

        if old_goods_price != price:
            change_price = ChangePrice(goods=goods, old_price=old_goods_price, new_price=price, updater=user)
            change_price.save()

        return HttpResponse(goods.name)


        # @login_required(login_url='/kucun/login')
        # def modal_diaoku(request):
        # if request.method == 'GET':
        # goods_id = request.GET.get('goods_id')
        # shop_id = request.GET.get('shop_id')
        # goodsshop = GoodsShop.objects.get(goods=Goods.objects.get(id=goods_id), shop=Shop.objects.get(id=shop_id))
        # return render_to_response('modal_diaoku.html', {'request': request, 'goodsshop': goodsshop})
        # elif request.method == 'POST':
        # return HttpResponse('post')


@login_required(login_url='/kucun/login')
def api_delete_goods_record(request):
    if request.method == 'POST':
        record_id = request.POST['record_id']
        reason = request.POST['reason']

        user = request.user

        goods_record = GoodsRecord.objects.get(id=record_id)
        if goods_record.change_num > 0 and reason == '1':
            return HttpResponse('cant_return')
        if goods_record.change_num < 0 and goods_record.sell_record:
            sell_record = goods_record.sell_record
            sell_record.is_delete = True
            sell_record.save()
        goods_record.is_delete = True
        goods_record.save()

        goods_shop = GoodsShop.objects.get(goods=goods_record.goods, shop=goods_record.shop)
        goods_shop.remain -= goods_record.change_num
        goods_shop.save()

        return_record = ReturnRecord(shop=goods_record.shop, goods=goods_record.goods, amount=goods_record.change_num,
                                     type=reason, updater=user)
        return_record.save()
        return HttpResponse('success')


@login_required(login_url='/kucun/login')
def out_in(request):
    shop = request.GET.get('shop')
    today = datetime.date.today()
    that_day_records = []
    header = title = ''
    if not shop:
        for i in range(0, 10):
            that_day = today - datetime.timedelta(days=i)
            goods_records = GoodsRecord.objects.filter(
                date__year=that_day.year, date__month=that_day.month,
                date__day=that_day.day, is_delete=False).order_by('-date')
            day_and_records_map = {'date': that_day, 'records': goods_records}
            that_day_records.append(day_and_records_map)
        title = header = '全部进出库'
    elif shop == 'guoao':
        for i in range(0, 10):
            that_day = today - datetime.timedelta(days=i)
            goods_records = GoodsRecord.objects.filter(
                date__year=that_day.year, date__month=that_day.month,
                date__day=that_day.day, shop__name='国奥店', is_delete=False).order_by('-date')
            day_and_records_map = {'date': that_day, 'records': goods_records}
            that_day_records.append(day_and_records_map)
        title = header = '国奥店进出库'
    elif shop == 'hongwei':
        for i in range(0, 10):
            that_day = today - datetime.timedelta(days=i)
            goods_records = GoodsRecord.objects.filter(
                date__year=that_day.year, date__month=that_day.month,
                date__day=that_day.day, shop__name='红卫店', is_delete=False).order_by('-date')
            day_and_records_map = {'date': that_day, 'records': goods_records}
            that_day_records.append(day_and_records_map)
        title = header = '红卫店进出库'
    elif shop == 'dadian':
        for i in range(0, 10):
            that_day = today - datetime.timedelta(days=i)
            goods_records = GoodsRecord.objects.filter(
                date__year=that_day.year, date__month=that_day.month,
                date__day=that_day.day, shop__name='大店', is_delete=False).order_by('-date')
            day_and_records_map = {'date': that_day, 'records': goods_records}
            that_day_records.append(day_and_records_map)
        title = header = '大店进出库'
    return render_to_response('out_in.html',
                              {'request': request, 'that_day_records': that_day_records, 'header': header,
                               'title': title})


@login_required(login_url='/kucun/login')
def check_out_in(request):
    if request.method == 'GET':
        return render_to_response('check_out_in_select_shop_date.html', {'title': '进出库查询', 'header': '进出库查询'})
    elif request.method == 'POST':
        shop_name = request.POST.get('shop_name')  # value=""的情况下，不是传过来空字符串
        sdate = request.POST['date']
        select_date = datetime.datetime.strptime(sdate, '%Y-%m-%d')
        if shop_name:
            goods_records = GoodsRecord.objects.filter(shop__name=shop_name, date__year=select_date.year,
                                                       date__month=select_date.month,
                                                       date__day=select_date.day).order_by('-date')
        else:
            goods_records = GoodsRecord.objects.filter(date__year=select_date.year, date__month=select_date.month,
                                                       date__day=select_date.day).order_by('-date')
        return render_to_response('out_in_check.html',
                                  {'request': request, 'goods_records': goods_records, 'header': '查询结果',
                                   'title': '查询结果'})


@login_required(login_url='/kucun/login')
def transfer(request):
    today = datetime.date.today()
    every_day_records = []
    for i in range(0, 10):
        that_day = today - datetime.timedelta(days=i)
        that_day_records = TransferGoods.objects.filter(date__year=that_day.year,
                                                        date__month=that_day.month,
                                                        date__day=that_day.day).order_by('-date')
        day_and_records_map = {'date': that_day, 'records': that_day_records}
        every_day_records.append(day_and_records_map)
    return render_to_response('transfer.html',
                              {'request': request, 'every_day_records': every_day_records, 'header': '调库记录'})


@login_required(login_url='/kucun/login')
def change_price(request):
    change_prices = ChangePrice.objects.filter(date__gt=datetime.date.today() - datetime.timedelta(days=30)).order_by(
        '-date')
    return render_to_response('change_price.html',
                              {'request': request, 'change_prices': change_prices, 'header': '改价记录'})


def mybackup(request):
    # 现将今天之前备份过的置为不是最新
    today = datetime.date.today()
    old_backups = Backup.objects.filter(save_datetime__year=today.year, save_datetime__month=today.month,
                                        save_datetime__day=today.day)
    for old_backup in old_backups:
        old_backup.is_lastet = False
        old_backup.save()

    goodss = Goods.objects.order_by('name')
    for goods in goodss:
        guoao = GoodsShop.objects.get(goods=goods, shop__name='国奥店')
        dadian = GoodsShop.objects.get(goods=goods, shop__name='大店')
        hongwei = GoodsShop.objects.get(goods=goods, shop__name='红卫店')
        backup = Backup(goods_name=goods.name, goods_type=goods.goods_type, dadian_count=dadian.remain,
                        guoaodian_count=guoao.remain, hongweidian_count=hongwei.remain)
        backup.save()

    return HttpResponse('success')


@login_required(login_url='/kucun/login')
def check_backup(request):
    if request.method == 'GET':
        return render_to_response("check_backup_select_date.html",
                                  {'request': request, 'title': '历史查询', 'header': '历史查询'})
    elif request.method == 'POST':
        sdate = request.POST['date']
        select_date = datetime.datetime.strptime(sdate, '%Y-%m-%d')

        backups = Backup.objects.filter(save_datetime__year=select_date.year, save_datetime__month=select_date.month,
                                        save_datetime__day=select_date.day,
                                        is_lastet=True)

        for backup in backups:
            backup.all_count = backup.dadian_count + backup.guoaodian_count + backup.hongweidian_count
        title = u'%s年%s月%s日' % (select_date.year, select_date.month, select_date.day)
        shang = len(backups) / 3
        yu = len(backups) % 3
        if yu != 0:
            shang += 1
        return render_to_response('check_backup_result.html',
                                  {'request': request, 'backups1': backups[:shang],
                                   'backups2': backups[shang:shang * 2],
                                   'backups3': backups[shang * 2:], 'title': title, 'header': title})


def sell_ranking_chart(request):
    goodses = Goods.objects.filter(is_delete=False, goods_type=0)
    goods_count_arr = []
    for goods in goodses:
        sell_records = SellRecord.objects.filter(goods=goods, is_delete=False)
        count = 0
        for sell_record in sell_records:
            count += sell_record.amount
        goods_count_arr.append({'goods': goods, 'count': count})
        goods_count_arr.sort(lambda y, x: cmp(x['count'], y['count']))
    title = u'手机销售排行'
    return render_to_response('sell_ranking_chart.html',
                              {'request': request, 'goods_count_arr': goods_count_arr, 'title': title, 'header': title})


def api_setcolor(request):
    if request.method == 'GET':
        goods_id = request.GET.get('goods_id')
        shop_id = request.GET.get('shop_id')
        goodsshop = GoodsShop.objects.get(goods=Goods.objects.get(id=goods_id), shop=Shop.objects.get(id=shop_id))
        try:
            color = ShopPhoneColor.objects.get(goodsshop=goodsshop)
        except:
            color = None

        return render_to_response('modal_color_shop.html', {'request': request, 'goodsshop': goodsshop, 'color': color})
    elif request.method == 'POST':
        user = request.user
        if not user:
            return HttpResponse("false")
        else:
            goodsshop_id = request.POST['goodsshop_id']
            color = request.POST['color']
            goodsshop = GoodsShop.objects.get(id=goodsshop_id)

            try:
                goodsphone_color = ShopPhoneColor.objects.get(goodsshop=goodsshop)
            except:
                goodsphone_color = ShopPhoneColor(goodsshop=goodsshop)
            finally:
                goodsphone_color.color=color
                goodsphone_color.save()

            return HttpResponse('success')

def api_showcolor(request):
    if request.method == 'GET':
        goods_id = request.GET.get('goods_id')
        colors={}
        goods=Goods.objects.get(id=goods_id)
        try:
            colors['guoao']=ShopPhoneColor.objects.get(goodsshop=GoodsShop.objects.get(goods=goods, shop__name='国奥店'))
        except:
            colors['guoao']=''
        try:
            colors['dadian']=ShopPhoneColor.objects.get(goodsshop=GoodsShop.objects.get(goods=goods, shop__name='大店'))
        except:
            colors['dadian']=''
        try:
            colors['hongwei']=ShopPhoneColor.objects.get(goodsshop=GoodsShop.objects.get(goods=goods, shop__name='红卫店'))
        except:
            colors['hongwei']=''



        return render_to_response('modal_color_show.html', {'request': request, 'colors': colors, 'goods':goods})
    elif request.method == 'POST':
        pass

def return_record(request):
    if request.method == 'GET':
        return_records = ReturnRecord.objects.filter(date__gt=datetime.date.today() - datetime.timedelta(days=30)).order_by(
        '-date')

        return render_to_response('return_record.html',
                              {'request': request, 'return_records': return_records, 'header': '撤单记录'})

def single_goods_detail(request):
    goods_id = request.GET.get('goods_id')
    goods=Goods.objects.get(id=goods_id)
    goods_records = GoodsRecord.objects.filter(goods=goods).order_by('-date')
    return render_to_response('single_goods_detail.html',
                                  {'request': request, 'goods_records': goods_records, 'header': '日志查询',
                                   'title': '日志查询'})