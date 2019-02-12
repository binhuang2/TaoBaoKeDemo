__author__ = 'Administrator'
from django import template
from django.utils.safestring import mark_safe
register = template.Library()
@register.simple_tag

def getCouponNum(instance, coupon_info):
    return coupon_info.split('减')[1].split('元')[0]
