#!/usr/bin/python

import json
import datetime
from calendar import timegm
from faker import Factory
from faker.providers import internet,misc,person,address,date_time,user_agent
import random


class basket_orders:
    fake = Factory.create()
    fake.add_provider(misc)
    fake.add_provider(person)
    fake.add_provider(date_time)

    def __init__(self):
        self.base_stores_list = {'San Francisco': 35,'New York': 25,'Tel Aviv': 15,'London': 5,'Los Angeles': 5,'Texsas': 5,'Atlanta':1,'Paris':4,'Chicago':3,'Barcelona':2}
        self.stores_list = [k for k in self.base_stores_list for dummy in range(self.base_stores_list[k])]
        random.shuffle(self.stores_list, random.random)

        self.base_items = [{'name': 'Milk', 'dist':20 , 'price':6.5},
                           {'name': 'Ham', 'dist': 40 , 'price': 4.9},
                           {'name': 'Gum', 'dist': 3, 'price': 1.5},
                           {'name': 'Cheese', 'dist': 15, 'price': 10.2},
                           {'name': 'Meat', 'dist': 30, 'price': 12.5},
                           {'name': 'Ice Cream', 'dist': 10, 'price': 7.9},
                           {'name': 'Eggs', 'dist': 25, 'price': 8.5},
                           {'name': 'Oil', 'dist': 5, 'price': 8.2},
                           {'name': 'Onion', 'dist': 4, 'price': 2.1},
                           {'name': 'Fish', 'dist': 15, 'price': 10.5},
                           {'name': 'Nuts', 'dist': 10, 'price': 2.1},
                           {'name': 'Yogurt', 'dist': 5, 'price': 2.9},
                           {'name': 'Bread', 'dist': 20, 'price': 6.1},
                           {'name': 'Rice', 'dist': 8, 'price': 5.2},
                           {'name': 'Orange juice', 'dist': 5, 'price': 8.7},
                           {'name': 'Carrots', 'dist': 5, 'price': 2.5},
                           {'name': 'Cereal', 'dist': 4, 'price': 12.9},
                           {'name': 'Sweets', 'dist': 15, 'price': 7.2},
                           {'name': 'Wine', 'dist': 5, 'price': 15.5},
                           {'name': 'Grapes', 'dist': 5, 'price': 5.5},
                           {'name': 'Pineapple', 'dist': 2, 'price': 4.3},
                           {'name': 'Bamba', 'dist': 2, 'price': 3.4},
                           {'name': 'Bagel', 'dist': 4, 'price': 5.2},
                           {'name': 'Cola', 'dist': 10, 'price': 5.3}
                           ]
        self.items = [{'name': i['name'], 'price': i['price']} for i in self.base_items for f in range(i['dist'])]
        random.shuffle(self.items, random.random)

        self.payment_type_list = ['Credit Card','Cash','Check']

        self.base_shopper_gender_list = {'Male': 3,'Female': 7}
        self.shopper_gender_list = [k for k in self.base_shopper_gender_list for dummy in range(self.base_shopper_gender_list[k])]
        random.shuffle(self.shopper_gender_list, random.random)

        self.base_purchase_type_list = {'Online': 2, 'Physical': 8}
        self.purchase_type_list = [k for k in self.base_purchase_type_list for dummy in range(self.base_purchase_type_list[k])]
        random.shuffle(self.purchase_type_list, random.random)

        self.order_item=''
        self.order_price = 0.0
        self.basket = []
        self.cash_basket_items =[]
        self.order_num=0


    def SetEventDT(self):
        secs = self.fake.random_int(min=1, max=3)
        self.event_dt = self.event_dt + datetime.timedelta(seconds=secs)
        self.event_unix_ts = timegm(self.event_dt.timetuple())

    def SetOrder(self):
        order = {}
        order['basket_id'] = self.basket_id
        order['store'] = self.store
        order['payment_type'] = self.payment_type
        order['order_datetime'] = self.order_dt.strftime('%Y-%m-%d %H:%M:%S.000')
        order['order_ts'] = self.order_unix_ts
        order['shopper_gender'] = self.shopper_gender
        order['purchase_type'] = self.purchase_type
        order['item'] = self.order_item
        order['price'] = self.order_price
        order['qty'] = self.qty
        return json.dumps(order)


    def SetFirstOrder(self):
        self.basket = []
        self.basket_id = self.fake.uuid4()
        self.store = self.fake.random_element(elements=(self.stores_list))
        self.payment_type = self.fake.random_element(elements=(self.payment_type_list))
        self.shopper_gender = self.fake.random_element(elements=(self.shopper_gender_list))
        self.purchase_type = self.fake.random_element(elements=(self.purchase_type_list))
        self.order_dt = datetime.datetime.now()
        self.order_unix_ts = timegm(self.order_dt.timetuple())

    def GetOrderItem(self):
        tmp_item = self.fake.random_element(elements=(self.items))

        if self.order_num>0:
            if any(tmp_item['name'] in s for s in self.cash_basket_items):
                return self.GetOrderItem()

        return tmp_item


    def basket_orders(self):
        num_of_event_per_basket = self.fake.random_int(min=2, max=10)
        self.SetFirstOrder()

        for x in range(0, num_of_event_per_basket):
            tmp_item = self.GetOrderItem()
            self.order_item = tmp_item['name']
            self.order_price = tmp_item['price']
            self.qty = self.fake.random_int(min=1, max=4)
            self.basket.append(self.SetOrder())
            self.order_num +=1
            self.cash_basket_items.append(self.order_item)
