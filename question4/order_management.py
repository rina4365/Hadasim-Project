from flask import Flask, request, jsonify
import threading
from enum import Enum
from collections import OrderedDict


app = Flask(__name__)

suppliers_list = dict()
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

    def __str__(self):
        product_details = ', '.join([f"{product['product_name']}: {product['amount']}" for product in self.product_list])
        return f"Order ID: {self.order_number}, Status: {self.order_status.value}, Products: {product_details}"


class product:
    def __init__(self, name, price, min):
        self.name = name
        self.price = price
        self.minimum_to_order = min

    def __str__(self):
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

#------------------

def approve_order(order_number):
    if order_number in orders_list.keys():
        if orders_list[order_number].order_status == OrderStatus.PENDING:
            orders_list[order_number].order_status = OrderStatus.IN_PROGRESS
            return True    
    return False


def get_supplier_orders_list(supplier_name):
    results = []
    for order in orders_list.values():
        if order.supplier_name == supplier_name and order.order_status in [OrderStatus.IN_PROGRESS, OrderStatus.PENDING]:
            products = []
            for product in order.product_list:
                product_name = product.get("product_name")
                amount = product.get("amount")
                products.append({
                    "product_name": product_name,
                    "amount": amount
                })

            results.append({
                "order_number": order.order_number,
                "supplier_name": order.supplier_name,
                "status": order.order_status.name,
                "products": products
            })

    return results


def log_in(supplier_name):
        if supplier_name in suppliers_list.keys():
            print("exist")
            return True
        else:
            print("not exist")
            return False

def add_new_product(supplier_name, product_name, product_price, minimum_to_order):
    if supplier_name in suppliers_list.keys():
        suppliers_list[supplier_name].add_product(product_name, product_price, minimum_to_order)


def add_new_supplier(supplier_name,agent_name, phone_number):
    if supplier_name in suppliers_list.keys():
        print("supplier is already exist")
    else:
        new_supplier = supplier(supplier_name, agent_name, phone_number)
        suppliers_list[supplier_name] = new_supplier
        print("supplier added") 
        print(suppliers_list[supplier_name])


#-----------------------------------------------------

def add_to_order(new_order, product_name, amount):
    product_info = suppliers_list[new_order.supplier_name].products_list[product_name]
    price = float(product_info.price) * float(amount)
    new_order.product_list.append({"product_name": product_name, "amount": amount})
    #new_order.product_list.appeand({product_name, amount})
    new_order.price += price
    print("product added to order")


def create_order(supplier_name):
    if supplier_name in suppliers_list.keys():
        if not suppliers_list[supplier_name].products_list:
            print ("supplier not have products yet")
        
        global order_number 
        order_number += 1
        new_order = order(order_number, supplier_name)
        orders_list[order_number] = new_order
        product_names = list(suppliers_list[supplier_name].products_list.keys())
        print(product_names)
        
        while True:
            product_name = input("please enter which product you want to edit to your order: ")
            if product_name in suppliers_list[supplier_name].products_list.keys():
                amount = input("please enter amount of products")
                add_to_order(new_order, product_name, amount)
                choice = input("to add new product press 1, to exit press 2: ")
                if choice == "2":
                    break
            else:
                print("product not exist")
    else:
        print("supplier not exist")


def print_open_orders():
     if not orders_list:
         print("no open orders")
         return
     for order_id, order in orders_list.items():
        if order.order_status == OrderStatus.IN_PROGRESS or order.order_status == OrderStatus.PENDING:
            print(order)


def close_order(order_number):
    if order_number in orders_list.keys():
        if orders_list[order_number].order_status != OrderStatus.COMPLETED:
            orders_list[order_number].order_status = OrderStatus.COMPLETED
            print(f"order number {order_number} is changed to COMPLETED!")
        else:
            print("order is already with cpmleted status")
    else:
        print(f"there is no order number {order_number}")


@app.route('/send_message',  methods=['POST', 'GET'])
def handle_action():
    if request.method == 'POST':
        data = request.get_json()
        request_type = data.get("action")

        
        if request_type == "add new soplier":
            add_new_supplier(data.get("suppliern name"), data.get("agent"), data.get("phone"))
            return jsonify({"message": "new supplier added"})
        
        elif request_type == "log-in":
            print("trying to log in")
            supplier = data.get("suppliern name")
            if log_in(supplier):
                return jsonify("exist")
            return jsonify("not exist")
        
        elif request_type == "approve order":
                order_number = data.get("order number")
                if approve_order(int(order_number)):
                    return jsonify({"message": "order approved"})
                else:
                    return jsonify({"message": "Order not approved"})
                
        elif request_type == "add product":
            supplier_name = data.get("suppliern name")
            product_name = data.get("product name")
            product_price = data.get("product price")
            minimum_to_order = data.get("minimum")
            add_new_product(supplier_name,product_name,product_price, minimum_to_order)
            return jsonify({"message": "product added"})
        
        else:
            return jsonify({"error": "Unknown request type"}), 400
    elif request.method == 'GET':
        supplier_name = request.args.get('supplier_name') 
        if supplier_name:
            orders = get_supplier_orders_list(supplier_name) 
            return jsonify({"orders": orders})
        else:
            return jsonify({"error": "Supplier name is required"}), 400

  

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
            close_order(int(order_number))
        elif choice == "4":
            print("exit")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    threading.Thread(target=main_loop, daemon=True).start()
    app.run(port=5000)

