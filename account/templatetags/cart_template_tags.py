from django import template
from account.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, is_ordered=False)
        if qs.exists():
            order = qs[0]
            return order.items.count()
        return 0