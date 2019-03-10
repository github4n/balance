import time
import re

from util.MyUtil import from_time_stamp


class MyOrderInfo(object):
    def __init__(self, symbol="", order_type="", price=0, amount=0, base=0):
        self.orderId = ""
        self.symbol = symbol
        self.orderType = order_type
        self.price = price
        self.totalAmount = amount
        self.base = base
        self.totalDealAmount = 0
        self.amount = 0
        self.dealAmount = 0
        self.avgPrice = 0
        self.transaction = 0
        self.count = 0
        self.triggerSeconds = int(time.time())
        self.timestamp = from_time_stamp(self.triggerSeconds)
        self.canceled = 0

    def __repr__(self):
        data = [str(self.orderId), self.symbol, self.orderType,
                str(self.base),
                str(self.price),
                str(self.avgPrice),
                str(self.dealAmount),
                str(self.totalDealAmount),
                str(self.transaction),
                "[" + str(self.count) + "]",
                str(self.timestamp)]
        if self.canceled == 1:
            data.append('[已撤销]')
        return ' '.join(data)

    def set_order_id(self, order_id):
        self.orderId = order_id

    def set_price(self, price):
        self.price = price

    def set_avg_price(self, avg_price):
        self.avgPrice = avg_price

    def set_amount(self, amount):
        self.amount = amount

    def set_deal_amount(self, deal_amount):
        self.dealAmount = deal_amount

    def reset_total_deal_amount(self, deal_amount):
        self.totalDealAmount += deal_amount

    def set_transaction(self, trans_type):
        if trans_type == 'plus':
            self.transaction = round(self.transaction + self.dealAmount * self.avgPrice, 3)
        else:
            self.transaction = round(self.transaction - self.dealAmount * self.avgPrice, 3)

    def get_buy_amount(self, price, accuracy=2):
        return round(self.transaction / price, accuracy)

    def get_unhandled_amount(self, accuracy=2):
        return round(self.totalAmount - self.totalDealAmount, accuracy)

    def set_count(self, client):
        if client.mode == "transaction":
            count = round(abs(self.transaction) / client.transaction, 2)
        else:
            count = round(self.totalDealAmount / client.amount, 2)
        per_count = round(abs(self.transaction) / count * client.percentage / 100, 4)
        if self.orderType == client.TRADE_BUY:
            count -= 1
        self.count = round(((1 + count) * count / 2 * per_count), 3)

    def from_log(self, line):
        match_obj = re.match(r"(.*) (.*) (.*) (.*) (.*) (.*) (.*) (.*) (.*) (.*) (.* .*)", line, re.M | re.I)
        if match_obj:
            self.orderId = match_obj.group(1)
            self.symbol = match_obj.group(2)
            self.orderType = match_obj.group(3)
            self.base = float(match_obj.group(4))
            self.price = float(match_obj.group(5))
            self.avgPrice = float(match_obj.group(6))
            self.dealAmount = float(match_obj.group(7))
            self.totalAmount = float(match_obj.group(8))
            self.totalDealAmount = float(match_obj.group(8))
            self.amount = float(match_obj.group(8))
            self.transaction = float(match_obj.group(9))
            self.count = float(re.search("[0-9]+(.[0-9]+)?", match_obj.group(10)).group())
            self.timestamp = match_obj.group(11)
