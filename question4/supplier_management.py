from collections import OrderedDict
import requests


suppliers_list = dict()


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
    

def log_in(supplier_name):
    while True:
        if supplier_name in suppliers_list.keys():
            print("to see open orders press 1, to approve order press 2, to add new product press 3, to exit press 4")
            choice = input()
            if choice == "1":
                data = {"action": "see orders", "suppliern name": supplier_name}
                response = requests.post("http://localhost:5000/send_message", json=data)
                print("done")
            elif choice == "2":
                print("please enter order number")
                order_number = input()
                data = {"action": "approve order", "order number": order_number}
                response = requests.post("http://localhost:5000/send_message", json=data)
            elif choice == "3":
                product_name, product_price, minimum_to_order = input("Please enter your details (product_name, product_proce, minimum_to_order) separated by commas: ").split(',')
                suppliers_list[supplier_name].add_product( product_name, product_price, minimum_to_order)
                print(suppliers_list[supplier_name])
            elif choice == "4":
                return
            else:
                print("worng option, please try again")
        else:
            print("you dont have user yet, please first register")


def register_new_supplier(supplier_name, agent_name, phone_number):
    if supplier_name in suppliers_list.keys():
        print("supplier is already exist")
    else:
        new_supplier = supplier(supplier_name, agent_name, phone_number)
        suppliers_list[supplier_name] = new_supplier
        print("supplier added")


def main():
    my_supplier = supplier("Tnuva","Avi","050")
    my_supplier.add_product("milk",10,20)
    my_supplier.add_product("bread",5,30)
    suppliers_list["Tnuva"] = my_supplier
    while True:
        print("\nMenu")
        print("1.log in")
        print("2.register")
        print("3.Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            supplier_name = input("Enter your supplier name ")
            log_in(supplier_name)
        elif choice == "2":
            supplier_name, agent_name, phone_number = input("Please enter your details (supplier name, agent name, and phone number) separated by commas: ").split(',')
            register_new_supplier(supplier_name, agent_name, phone_number)
        elif choice == "3":
            print("exit")
            break

        else:
            print("Invalid choice, try again.")
        


if __name__ == "__main__":
    main()

