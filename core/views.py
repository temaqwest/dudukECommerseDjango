from django.shortcuts import render, get_object_or_404
from .models import Item, OrderItem, Order
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class itemView(ListView):
    model = Item
    template_name = "item_list.html"


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order.")
            return redirect("/")
    # template_name = 'order_summary.html'


def checkout(request):
    return render(request, "checkout.html")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
    # проверяем если товар находится в заказе
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was updated!')
            print(order_item)
        else:
            messages.info(request, 'This item was added to your cart!')
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This item was added to your cart!')
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # проверяем если товар находится в заказе
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, 'Item was deleted from your cart.')
        else:
            # сообщение, что у юзера нет айтемов в заказе
            messages.info(request, 'User dont have an items in order.')
            return redirect("core:product", slug=slug)
    else:
        #  сообщение у пользователя нет ордеров
        messages.info(request, 'User dont have an active order.')
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)
