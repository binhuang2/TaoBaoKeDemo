from m.shop_request import TbkRequest
import math

PAGE_SIZE = 12

class api():
    @classmethod
    def index(self,request):
        '''
           首页
           '''
        page_no = request.GET.get('page')

        # 页码
        if page_no is None or len(page_no) == 0:
            page_no = 1
        param = {
            'method': 'taobao.tbk.dg.optimus.material',
            'adzone_id': '91132500175',
            'material_id': 9660,
            'page_no': page_no,
            'page_size': PAGE_SIZE
        }
        res = TbkRequest.TbkDgOptimusMaterialRequest(param).getResponse()
        if res is False:
            return False

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
            'res': res
        }
        return data

    @classmethod
    def search(self, request):
        '''
        搜索
        :param request:
        :return:
        '''
        # 页码
        page_no = request.GET.get('page')
        # 搜索关键字
        q = request.GET.get('q')

        if page_no is None or len(page_no) == 0:
            page_no = 1
        if q is None or len(q) == 0:
            q = '面包'
        param = {
            'method': 'taobao.tbk.dg.material.optional',
            'q': q,
            'adzone_id': '91132500175',
            'platform': 2,
            'page_no': page_no,
            'page_size': PAGE_SIZE
        }

        # 调用淘宝客接口
        res = TbkRequest.TbkDgMaterialOptionalRequest(param).getResponse()
        map_data = res['result_list']['map_data']
        coupon = []
        for values in map_data:
            values['pict_url'] = values['pict_url'].replace('\\', '')
            if len(values['coupon_id']) > 0:
                values['coupon_share_url'] = values['coupon_share_url'].replace('\\', '')
                coupon_info = values['coupon_info'].split('减')[1]
                values['coupon_info'] = coupon_info
                current_price = '%.2f' % (float(values['zk_final_price']) - float(coupon_info.split('元')[0]))
                values['current_price'] = current_price
                coupon.append(values)

        data = {
            'q': q
        }

        if res is False:
            return False

            # 计算分页
        if 'total_results' in res:
            data['page_count'] = math.ceil(int(res['total_results']) / PAGE_SIZE)
        data['res'] = coupon
        print(data)
        return data