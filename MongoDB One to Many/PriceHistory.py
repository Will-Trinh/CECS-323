from mongoengine import *
from datetime import *
from decimal import *


class PriceHistory(EmbeddedDocument):
    price = Decimal128Field(db_field='new_price', min_value=0.01, precision=2, required=True)
    priceChangeDate = DateTimeField(db_field='price_change_date', required=True)

    def __init__(self, price: Decimal, price_change_date: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.price = price
        self.priceChangeDate = price_change_date

    def __str__(self):
        return (f'New Price: {self.price} \n'
                f'Price Change Date: {self.priceChangeDate}\n')
