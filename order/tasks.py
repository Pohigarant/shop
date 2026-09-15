from celery import shared_task
from django.core.mail import send_mail

from order.models import Order


@shared_task
def send_order_confirmation(order_id):
    order = Order.objects.select_related("user").get(pk=order_id)
    send_mail(
        subject=f"Заказ №{order_id} принят",
        message=f"Сумма заказа:  {order.total_price} ₽",
        from_email="",
        recipient_list=["Pohigarant@mail.ru"],
    )
