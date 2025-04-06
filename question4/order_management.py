from flask import Flask, request, jsonify
import threading
from enum import Enum

app = Flask(__name__)

orders_list = dict()
order_number = 0


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


# class supplier:
#     def __init__(self, supplier_name, agent_name, phone_number):
#         self.supplier_name = supplier_name
#         self.agent_name = agent_name
#         self.phone_number = phone_number
#         self.products_list = OrderedDict()

# def add_new_product(product):
#     if product.supplier_name in products_dict.keys():
#        # products_dict[product.supplier_name]
#     else:
#         products_dict[product.supplier_name] = product





def add_to_order(new_order, product_name, amount):
    price = product.price * amount
    new_order.product_list.appeand({product, amount})
    new_order.price += price


def create_order(supplier_name):
    global order_number 
    order_number += 1
    new_order = order(order_number, supplier_name)
    orders_list[order_number] = new_order
    products_list = suppliers_list[supplier_name].products_list
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


@app.route('/action', methods=['POST'])
def handle_action():
    data = request.get_json()
    request_type = data.get("type")

    if request_type == "see orders":
        name = data["supplier name"]
        return jsonify({"message": f"Order {order_id} confirmed."})

    elif request_type == "approve order":
        order_id = data["order number"]
        return jsonify({"message": f"Order {order_id} confirmed."})

    else:
        return jsonify({"error": "Unknown request type"}), 400
    

def main_loop():
    while True:
        print("\nMenu")
        print("1.create new order")
        print("2.see open orders")
        print("3.close order")
        print("4.exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            supplier_name = input("please enter from which supplier you want to order: ")
            create_order(supplier_name)
        elif choice == "2":
            print_open_orders()
        elif choice == "3":
            order_number = input("please enter order number: ")
            close_order(order_number)
        elif choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    threading.Thread(target=main_loop, daemon=True).start()
    app.run(port=5000)

