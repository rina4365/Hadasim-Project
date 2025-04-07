from collections import OrderedDict
import requests


def supplier_actions(supplier_name):
    while True:
        print("to see open orders press 1, to approve order press 2, to add new product press 3, to exit press 4")
        choice = input()
        if choice == "1":
            response = requests.get(f"http://localhost:5000/send_message?supplier_name={supplier_name}")
    
            if response.status_code == 200:
                orders = response.json() 
                
                print(f"Orders for {supplier_name}:")
                if orders == []:
                     print(f"No orders found for supplier {supplier_name}.")
                else: 
                    print(orders)
            else:
                print("Failed to retrieve orders.")
                
        elif choice == "2":
            print("please enter order number")
            order_number = input()
            data = {"action": "approve order", "order number": order_number}
            response = requests.post("http://localhost:5000/send_message", json=data)
            response_json = response.json()
            print(response_json["message"])
        
        elif choice == "3":
            product_name, product_price, minimum_to_order = input("Please enter your details (product_name, product_proce, minimum_to_order) separated by commas: ").split(',')
            data = {"action": "add product", "suppliern name": supplier_name,
                    "product name": product_name, "product price": product_price, "minimum": minimum_to_order}
            response = requests.post("http://localhost:5000/send_message", json=data)
            response_json = response.json()
            print(response_json["message"])

        elif choice == "4":
            return
        
        else:
            print("worng choice, try again")
        

def log_in(supplier_name):
    data = {"action": "log-in", "suppliern name": supplier_name}
    response = requests.post("http://localhost:5000/send_message", json=data)
    if response.json() == "exist":
        supplier_actions(supplier_name)
    else:
        print("you dont have user yet, please register")


def register_new_supplier(supplier_name, agent_name, phone_number):
    data = {"action": "add new soplier", "suppliern name": supplier_name,"agent": agent_name, "phone": phone_number }
    response = requests.post("http://localhost:5000/send_message", json=data)
    print("Response Content:", response.text)


def main():
    supplier_data = [
    ("Tnuva", "Dana", "052-1234567"),
    ("Osem", "Yossi", "052-7654321"),
    ("Elite", "Rina", "054-1112233"),
    ("Strauss", "Amit", "053-3334444"),
    ("Tara", "Noa", "052-9998888")
    ]   
    for name, agent, phone in supplier_data:
        register_new_supplier(name,agent,phone)
        
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

