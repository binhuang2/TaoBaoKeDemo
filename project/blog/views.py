from django.shortcuts import render
from blog.shop_request import TbkRequest
# Create your views here.

def index(request):
    return render(request, 'index.html')

def search(request):
    product_name = request.GET.get('q')
    if product_name is None:
        product_name = '面包'
    param = {
        'method':'taobao.tbk.dg.material.optional',
        'q':product_name,
        'adzone_id':'91132500175',
        'platform':2
    }
    req = TbkRequest.TbkDgMaterialOptionalRequest(param)
    res = req.getResponse()
    data = {
        'q':product_name
    }
    if res is not False:
        map_data = res['result_list']['map_data']
        coupon = []
        not_coupon = []
        for values in map_data:
            if len(values['coupon_id']) > 0:
                values['coupon_share_url'] = values['coupon_share_url'].replace('\\','')
                values['coupon_info'] = values['coupon_info'].split('减')[1]
                coupon.append(values)
            else:
                not_coupon.append(values)
        res = []
        res.extend(coupon)
        res.extend(not_coupon)
        data['res'] = res
    return render(request, 'search.html', {'data' : data})