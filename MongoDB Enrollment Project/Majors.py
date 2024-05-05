from mongoengine import *

class Major(Document):

    customerName = StringField(db_field='customer_name', max_length=80, min_length=5, required=True)
    
    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['customerName', 'orderDate'], 'name': 'orders_pk'}
            ]}
    
    def __init__(self):
        pass

    def __str__(self):
        pass