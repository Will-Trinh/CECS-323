from mongoengine import *
from PriceHistory import PriceHistory
from datetime import *
from decimal import *
#Test

class Product(Document):
    productCode = StringField(db_field="product_code", min_Length=0, max_length=15, required=True)
    productName = StringField(db_field="product_name", min_Length=0, max_length=70, required=True)
    productDescription = StringField(db_field="product_description", min_Length=0, max_length=800, required=True)
    qualityInStock = IntField(db_field="quality_in_stock", min_value=0.01, precision=2, required=True)
    buyPrice = Decimal128Field(db_field='buy_price', min_value=0.01, precision=2, required=True)
    msrp = Decimal128Field(db_field='msrp', min_value=0.01, precision=2, required=True)
    priceHistory = EmbeddedDocumentListField(PriceHistory, db_field='price_history')


    meta = {'collection': 'products',
            'indexes': [
                {'unique': True, 'fields': ['productCode'], 'name': 'products_uk_01'},
                {'unique': True, 'fields': ['productName'], 'name': 'products_uk_02'}
            ]}

    def __init__(self, productCode, productName, productDescription, quantityInStock, buyPrice, msrp, *args, **values):
        super().__init__(*args, **values)
        self.productCode = productCode
        self.productName = productName
        self.productDescription = productDescription
        self.quantityInStock = quantityInStock
        self.buyPrice = buyPrice
        self.msrp = msrp

    def change_price(self, new: PriceHistory):
        if not self.priceHistory:
            self.priceHistory = [PriceHistory(self.buyPrice, datetime(1, 1, 1, 1, 1))]

        # Make sure that the new price is different from the old one
        if self.priceHistory[-1].price == new.price:
            raise ValueError("New price must be different than current price.")

        # Make sure that the new price is not < $.01
        elif new.price < Decimal(0.01):
            raise ValueError("New price must be greater than or equal to $0.01.")

        # Make sure that the change date doesn't take place in the future or during a date before the last change date
        elif new.priceChangeDate > datetime.utcnow():
            raise ValueError("This price change date cannot be in the future.")
        elif self.priceHistory[-1].priceChangeDate >= new.priceChangeDate:
            raise ValueError("New price change date must take place after last price change date")

        self.priceHistory.append(new)
        self.buyPrice = new.price

    def __str__(self):
        return (f"Name: {self.productName} \n"
                f"Code: {self.productCode} \n"
                f"Description: {self.productDescription}\n"
                f"Quantity in Stock: {self.quantityInStock} \n"
                f"Price: ${self.buyPrice} \n"
                f"MSRP: ${self.msrp} \n")




