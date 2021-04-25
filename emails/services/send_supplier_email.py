from django.core.mail import send_mail
from emails.models import OrderEmail

def send_email_to_supplier(
    *,
    inventory_ingredient_target : InventoryIngredient,
    email_text: str
)

