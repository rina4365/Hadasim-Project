from flask import Flask, request, jsonify
import threading
from enum import Enum
from collections import OrderedDict


app = Flask(__name__)

orders_list = dict()
order_number = 0
suppliers_list = dict()


class OrderStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class order:
    def __init__(self, number, supplier_name):
        self.order_number = number
        self.product_list = []
        self.price = 0
        self.supplier_name = supplier_name
        self.order_status = OrderStatus.PENDING


class product:
    def __init__(self, name, price, min):
        self.name = name
        self.price = price
        self.minimum_to_order = min

    def __str__(self):
        # Custom print format for each product
        return f"Product: {self.name}, Price: {self.price}, Minimum Order: {self.minimum_to_order}"


class supplier:
    def __init__(self, supplier_name, agent_name, phone_number):
        self.supplier_name = supplier_name
        self.agent_name = agent_name
        self.phone_number = phone_number
        self.products_list = OrderedDict()


    def __str__(self):
        # Custom print format for supplier details and products
        product_details = ", ".join([f"{key}: {value}" for key, value in self.products_list.items()])
        return f"Supplier: {self.supplier_name}, Agent: {self.agent_name}, Phone: {self.phone_number}, Products: [{product_details}]"


    def add_product(self,product_name, product_price, product_min_amount):
        new_product = product(product_name, product_price, product_min_amount)
        self.products_list[product_name] = new_product


def add_to_order(new_order, product_name, amount):
    price = product.price * amount
    new_order.product_list.appeand({product, amount})
    new_order.price += price


def create_order(supplier_name):
    global order_number 
    order_number += 1
    new_order = order(order_number, supplier_name)
    orders_list[order_number] = new_order
    products_list = orders_list[supplier_name].products_list
    print(products_list)
    #add_to_order(new_order, product_name)


def print_open_orders():
    for order in orders_list:
        if order.order_status == OrderStatus.IN_PROGRESS or order.order_status == OrderStatus.PENDING:
            print(order)


def close_order(order_number):
    if order_number in orders_list.keys():
        if orders_list[order_number].order_status != OrderStatus.COMPLETED:
            orders_list[order_number].order_status = OrderStatus.COMPLETED
            print(f"order number {order_number} is changed to COMPLETED!")
    else:
        print(f"there is no order number {order_number}")

def add_new_supplier(supplier_name,agent_name, phone_number):
    if supplier_name in suppliers_list.keys():
        print("supplier is already exist")
    else:
        new_supplier = supplier(supplier_name, agent_name, phone_number)
        suppliers_list[supplier_name] = new_supplier
        print("supplier added")

# def main_loop():
#     while True:
#         print("\nMenu")
#         print("1.create new order")
#         print("2.see open orders")
#         print("3.close order")
#         print("4.exit")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             supplier_name = input("please enter from which supplier you want to order: ")
#             create_order(supplier_name)
#         elif choice == "2":
#             print_open_orders()
#         elif choice == "3":
#             order_number = input("please enter order number: ")
#             close_order(order_number)
#         elif choice == "4":
#             print("exit")
#             break

#         else:
#             print("Invalid choice, try again.")


@app.route('/action', methods=['POST'])
def handle_action():
    data = request.get_json()
    request_type = data.get("action")

    if request_type == "see orders":
        return jsonify({"message": "Order confirmed."})

    elif request_type == "approve order":
        order_id = data["order number"]
        return jsonify({"message": "Order confirmed."})
    
    elif request_type == "add new soplier":
        add_new_supplier(data.get("suppliern name"), data.get("agent"), data.get("phone"))
        return jsonify({"message": "Order confirmed."})
    
    else:
        return jsonify({"error": "Unknown request type"}), 400
    

# 

if __name__ == "__main__":
    # threading.Thread(target=main_loop, daemon=True).start()
    app.run(port=5000)

