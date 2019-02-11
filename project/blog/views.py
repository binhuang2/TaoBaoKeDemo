from django.shortcuts import render
from blog.shop_request import TbkRequest
# Create your views here.

def index(request):
    product_name = request.GET.get('product_name')
    data = {}
    if (product_name):
        param = {'method':'taobao.tbk.item.get', 'q':product_name, 'fields':'title'}
        req = TbkRequest.TbkItemGetRequest(param)
        res = req.getResponse()
        if res != False:
            data = {'product_name': product_name, 'result': res}
    return render(request, 'index.html', {'data' : data})