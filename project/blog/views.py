from django.shortcuts import render
from blog.shop_request import TbkRequest
from blog.plugs import JXPlugs
import math
# Create your views here.

#定义一些常量
#每页数据的数量
PAGE_SIZE = 20


#view code

def index(request):
    '''
    首页
    '''
    return render(request, 'index.html')

def search(request):
    '''
    搜索页面
    '''
    product_name = request.GET.get('q')
    page_no = request.GET.get('page')

    #页码
    if page_no is None:
        page_no = 1

    #搜索关键字
    if product_name is None:
        product_name = '面包'

    param = {
        'method':'taobao.tbk.dg.material.optional',
        'q':product_name,
        'adzone_id':'91132500175',
        'platform':2,
        'page_no':page_no,
        'page_size':PAGE_SIZE
    }

    #调用淘宝客接口
    req = TbkRequest.TbkDgMaterialOptionalRequest(param)
    res = req.getResponse()
    data = {
        'q':product_name
    }

    if res is False:
        return render(request, 'search.html', data)

    #计算分页
    '''math.ceil(int(res['total_results']) / PAGE_SIZE)'''
    page_count = 21
    page_object = JXPlugs.page(page_count)
    page_list = page_object.comput(int(page_no))

    data['page'] = {
        'list' : page_list,
        'start_page' : page_object.current_start_page,
        'end_page' : page_object.current_end_page,
        'previous':page_object.current_page - 1,
        'p' : page_object.current_page,
        'next': page_object.current_page + 1,
        'count':page_count
    }

    map_data = res['result_list']['map_data']
    coupon = []
    not_coupon = []
    for values in map_data:
        if len(values['coupon_id']) > 0:
            values['coupon_share_url'] = values['coupon_share_url'].replace('\\','')
            coupon_info = values['coupon_info'].split('减')[1]
            values['coupon_info'] = coupon_info
            current_price = '%.2f' % (float(values['zk_final_price']) - float(coupon_info.split('元')[0]))
            values['current_price'] = current_price
            coupon.append(values)
        else:
            not_coupon.append(values)
    res = []
    res.extend(coupon)
    res.extend(not_coupon)
    data['res'] = res
    return render(request, 'search.html', {'data' : data})