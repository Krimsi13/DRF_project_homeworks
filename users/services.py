import stripe
from config.settings import STRIPE_APY_KEY

stripe.api_key = STRIPE_APY_KEY


def create_stripe_product(product):
    """Создает продукт в cтрайпе"""

    return stripe.Product.create(name=product)

# можно сделать конвертацию из доллара в рубли
# def convert_rub_to_usd(amount):
#     pass


def create_stripe_price(amount, product):
    """Создает цену в страйпе."""

    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": product},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе."""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")
