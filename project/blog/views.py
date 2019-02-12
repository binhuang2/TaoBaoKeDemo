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
        'adzone_id':'91132500175'
    }
    req = TbkRequest.TbkDgMaterialOptionalRequest(param)
    res = req.getResponse()
    data = {}
    if res is not False:
        data = {'q': product_name, 'res': res}
    return render(request, 'search.html', {'data' : data})