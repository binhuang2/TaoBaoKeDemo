from django.shortcuts import render
from django.shortcuts import HttpResponse
from blog.shop_request import TbkRequest
from blog.plugs import JXPlugs
import math

# Create your views here.

#定义一些常量
#每页数据的数量
PAGE_SIZE = 12

#view code

def index(request):
    '''
    首页
    '''
    page_no = request.GET.get('page')

    #页码
    if  page_no is None or len(page_no) == 0:
        page_no = 1
    param = {
        'method': 'taobao.tbk.dg.optimus.material',
        'adzone_id': '91132500175',
        'material_id':9660,
        'page_no': page_no,
        'page_size': PAGE_SIZE
    }
    res = TbkRequest.TbkDgOptimusMaterialRequest(param).getResponse()
    if res is False:
        return render(request, 'index.html')

    map_data = res['result_list']['map_data']
    coupon = []
    not_coupon = []
    for values in map_data:
        values['pict_url'] = values['pict_url'].replace('\\', '')
        if len(values['coupon_click_url']) > 0:
            values['coupon_share_url'] = values['coupon_click_url'].replace('\\', '')
            current_price = values['coupon_amount']
            values['coupon_info'] = '%s元' % current_price
            values['current_price'] = '%.2f' % (float(values['zk_final_price']) - float(current_price))
            coupon.append(values)
        else:
            not_coupon.append(values)
    res = []
    res.extend(coupon)
    res.extend(not_coupon)
    data = {
        'res':res
    }
    page_count = math.ceil(100 / PAGE_SIZE)
    page_object = JXPlugs.page(page_count)
    page_list = page_object.comput(int(page_no))
    data['page'] = {
        'list': page_list,
        'start_page': page_object.current_start_page,
        'end_page': page_object.current_end_page,
        'previous': page_object.current_page - 1,
        'p': page_object.current_page,
        'next': page_object.current_page + 1,
        'count': page_count
    }
    return render(request, 'index.html', {'data': data})


def search(request):
    '''
    搜索页面
    '''
    product_name = request.GET.get('q')
    page_no = request.GET.get('page')

    #页码
    if  page_no is None or len(page_no) == 0:
        page_no = 1

    #搜索关键字
    if product_name is None or len(product_name) == 0:
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
    res = TbkRequest.TbkDgMaterialOptionalRequest(param).getResponse()
    data = {
        'q':product_name
    }

    if res is False:
        return render(request, 'search.html', data)

    #计算分页
    if 'total_results' in res:
        page_count = math.ceil(int(res['total_results']) / PAGE_SIZE)
        page_object = JXPlugs.page(page_count)
        page_list = page_object.comput(int(page_no))
        data['page'] = {
            'list': page_list,
            'start_page': page_object.current_start_page,
            'end_page': page_object.current_end_page,
            'previous': page_object.current_page - 1,
            'p': page_object.current_page,
            'next': page_object.current_page + 1,
            'count': page_count
        }


    map_data = res['result_list']['map_data']
    coupon = []
    not_coupon = []
    for values in map_data:
        values['pict_url'] = values['pict_url'].replace('\\', '')
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

def page_not_found(request):
    return render(request, '404.html')

def page_inter_error(request):
    return render(request, '500.html')