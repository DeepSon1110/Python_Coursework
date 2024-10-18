import datetime
import operation
import read
VAT_RATE = 0.13  # 13% VAT

def read_file():
    """
    Read the file and return the data.
    
    Returns:
        list:  A list of dictionaries, where each dictionary represents a furniture items.
            Returns empty list if file not found
    """
    try:
        with open("Furniture.txt", 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print("File not found")
        return []

def buy_furniture():
    """
    Handling the process of Buying furniture from the file.
    -Displays available furniture.
    -Asks user to select the furnitureID, quantity, name to buy furniture.
    -updates list, calculate totalPrice, price including vat and shipping cost and generates invoice.
    
    """
    
    furniture_list = read_file()
    
    #displays available furniture
    read.display_available_furniture(furniture_list)
    
    #set total price as o and transactions as empty list
    total_price = 0
    transactions = []

    #getting employee name for buying process
    while True:
        employee_name = input("Enter the name of the employee who is purchasing this order: ")

        # Check if the input contains only alphabetic characters
        if employee_name.isdigit():
            print("Invalid Input. Employee name cannot be a number")
        elif not all(char.isalpha() or char.isspace() for char in employee_name):
            print("Invalid Input. Employee name must be alphabets only")
        else:
            break


    #further processing 
    while True:
        #getting and validating the furniture ID
        try:
            furniture_id = int(input("Enter the furniture ID: "))
            if furniture_id <= 0:
                print("Invalid ID.Furniture id must be positive number.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        furniture_id_found = False
        for furniture in furniture_list:
            values = furniture.strip().split(", ")
            if int(values[0]) == furniture_id:
                furniture_id_found = True
                break
            
        if not furniture_id_found:
            while True:
                add_new_furniture = input(f"Furniture ID: {furniture_id} not found. Do you want to add new furniture with this ID ?  (yes/no) : ")
                if add_new_furniture.lower() not in ['yes','no']:
                    print("Invalid input. Please enter yes or no.")
                else:
                    break
            if add_new_furniture.lower() == "yes":
                #adding new furniture details
                name = input("Enter the name of the furniture: ")
                manufacturer_name = input("Enter the manufacturer name: ")
                while True:
                    try:
                        quantity = int(input("Enter the quantity: "))
                        if quantity <= 0:
                            print("Invalid quantity. Quantity must be positive")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                while True:
                    try:
                        price_per_item = float(input("Enter the price per item: "))
                        if price_per_item <= 0:
                            print("Invalid price. Price must be positive ")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                #add new furniture to the list and write it to the file
                new_furniture = f"{furniture_id}, {manufacturer_name}, {name}, {quantity}, {price_per_item}"
                furniture_list.append(new_furniture)
                with open("Furniture.txt", 'a') as file:
                    file.write(new_furniture + "\n")
            else:
                print("furniture id does not match.Returning to main menu....")
                return
                
        else:
            #getting and validating the Quantity
            try:
                quantity = int(input("Enter the quantity: "))
                if quantity <= 0:
                    print("Invalid quantity. Quantity must be positive number.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
        
        try:
            furniture_list = read_file()
            updated_data = []
            manufacturer_name = ""
            name = ""
            price_per_item = ""

            #updating list with purchased quantity
            for furniture in furniture_list:
                values = furniture.strip().split(", ")
                if int(values[0]) == furniture_id:
                    values[3] = str(int(values[3]) + quantity)
                    furniture_id = values[0]
                    manufacturer_name = values[1]
                    name = values[2]
                    price_per_item = values[4]
                    updated_data.append(", ".join(values))
                else:
                    updated_data.append(", ".join(values))
            
            #calculating the price for purchase       
            price = operation.calculate_price(price_per_item, quantity)
            total_price += price

            #writing the updated inventory back to file
            with open("Furniture.txt", 'w') as file:
                for data in updated_data:
                    file.write(data + "\n")

            #recording the transactions
            transactions.append({
                "furniture_id": furniture_id,
                "name": name,
                "manufacturer_name": manufacturer_name,
                "quantity": quantity,
                "price": price
            })
            
            #asking the user if they want to add another items to the invoice
            while True:
                response = input("Do you want to add another item to the invoice? (yes/no): ")
                if response.lower() not in ['yes','no']:
                    print("Invalid input.please enter 'yes' or 'no'.")
                else:
                    break
            if response.lower() == 'no':
                break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    #asking they want to add shipping cost or not      
    while True:
        add_shipping = input("Do you want to add shipping cost? (yes/no): ")
        if add_shipping.lower() not in ['yes','no']:
            print("Invalid input.please enter 'yes' or 'no'.")
            continue
        if add_shipping == 'yes':
            try:
                shipping_cost = float(input("Enter shipping cost: $"))
                if shipping_cost < 0:
                    print("Shipping cost cannot be negative.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue
        else:
            shipping_cost = 0.00
        break
    
    #calculating VAT and total Price
    vat_amount = total_price * VAT_RATE
    total_price += vat_amount + shipping_cost

    #genrating the invoice
    generate_invoice(transactions, employee_name, total_price, shipping_cost, vat_amount)


def generate_invoice(transactions, employee_name, total_price, shipping_cost, vat_amount):
    """
    Generate and display an invoice
    
    Args:
        transactions (list): A list of dictionaries containing transaction details of purchased item.
        employee_name (str): name of employee who made purchase
        total_price (float): total price of the invoice
        shipping_cost (float): shipping cost of the invoice
        vat_amount (float): VAT amount of the invoice
        
    """
    invoice_text = f"""\
==============================================================================================
                                   BRJ Furniture Store    
                                        INVOICE    
==============================================================================================

Employee Details:
----------------------------------------------------------------------------------------------
Name: {employee_name}
Date and Time of Purchase: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==============================================================================================

Purchased Items:
----------------------------------------------------------------------------------------------
| No | Furniture ID |     Manufacturer Name        |  Product Name  |  Quantity  |    Price |
----------------------------------------------------------------------------------------------
"""
    count = 1
    for transaction in transactions:
        invoice_text += f"| {count:<3} | {transaction['furniture_id']:<11} | {transaction['manufacturer_name']:<28} | {transaction['name']:<14} | {transaction['quantity']:<10} | ${transaction['price']:<6.2f} |\n"
        count += 1

    invoice_text += """----------------------------------------------------------------------------------------------
"""

    invoice_text += f"""
----------------------------------------------------------------------------------------------
SubTotal:                       ${total_price - vat_amount - shipping_cost:.2f}
VAT (13%):                      ${vat_amount:.2f}
Shipping Cost:                  ${shipping_cost:.2f}
----------------------------------------------------------------------------------------------
Total Amount:                   ${total_price:.2f}
==============================================================================================

                               THANK YOU FOR SHOPPING WITH US!
==============================================================================================
"""

    #displaying the invoice
    print(invoice_text)
    
    #saving the invoice to a file
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") +"-" + "purchase" +"_invoice.txt"
    with open(filename, "w") as file:
        file.write(invoice_text)
        print("Transactions Successfully Conducted.")


       
def sell_furniture():
    """
    Handling the process of selling furniture:
    -displaying available furniture.
    -ask user to input customer name, furnitureId, quantity and other details.
    -updates inventory, calculates total price including vat and shipping cost and generates and display invoice.
    """
    furniture_list = read_file()
    
    #displaying the available furnitures
    read.display_available_furniture(furniture_list)
    
    total_price = 0
    transaction1 =[]
    
    #getting user name as input
    while True:
        customer_name = input("Enter the name of the employee who is purchasing this order: ")
        
        # Check if the input contains only alphabetic characters
        if customer_name.isdigit():
            print("Invalid Input. customer name cannot be a number")
        elif not all(char.isalpha() or char.isspace() for char in customer_name):
            print("Invalid Input. customer name must be alphabets only")
        else:
            break
    
    # Getting and validating the phone number
    while True:
        phone_number = input("Enter phone number (10 digits): ")
        if phone_number.isdigit() and len(phone_number) == 10:
            break
        else:
            print("Invalid phone number. Please enter a 10-digit number.")
    
    # Getting the address as input
    address = input("Enter address: ")
                
    #processing each furniture sale
    while True:
        #getting and validating the furniture ID
        try:
            furniture_id = int(input("Enter the furniture ID: "))
            if furniture_id < 0:
                print("Please enter a valid ID.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid furniture ID.")
            continue
        
        found = False
        for furniture in furniture_list:
            values = furniture.strip().split(", ")
            if int(values[0]) == furniture_id:
                found = True
                break
            
        if not found:
            print(f"Invalid Furniture ID: {furniture_id} does not exist. Please enter a correct ID.")
            continue
        
        #getting and validating the quantity
        try:
            quantity = int(input("Enter the quantity: "))
            if quantity <= 0:
                print("Please enter a valid quantity.")
                continue
        except ValueError:
            print("Invalid input.please enter a valid input.")
            continue
            
            
        try:
            #updating inventory
            furniture_list = read_file()
            new_data = []
            manufacturer_name = ""
            name = ""
            price_per_item = ""

            for furniture in furniture_list:
                values = furniture.strip().split(", ")
                if int(values[0]) == furniture_id:
                    if int(values[3]) >= quantity:
                        values[3] = str(int(values[3]) - quantity)
                        manufacturer_name = values[1]
                        name = values[2]
                        price_per_item = values[4]
                        new_data.append(", ".join(values))
                    else:
                        print("Insufficient quantity of furniture available to fulfill the order.")
                        return
                else:
                    new_data.append(", ".join(values))

            #calculating the price for the transactions
            price = operation.calculate_price(price_per_item, quantity)
            total_price += price
            
            #writing the updated inventory back in the file
            with open("Furniture.txt", 'w') as file:
                for data in new_data:
                    file.write(data + "\n")

            #storing the transactions details
            transaction1.append({
                "furniture_id": furniture_id,
                "name": name,
                "manufacturer_name": manufacturer_name,
                "quantity": quantity,
                "price": price,
            })
            
            #asking the user to add another items to the invoice
            while True:
                response = input("Do you want to add another item to the invoice? (yes/no): ")
                if response.lower() not in ['yes','no']:
                    print("Invalid input. Please enter 'yes' or 'no'.")
                else:
                    break
            if response.lower() == 'no':
                break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    #asking if the user want to add shipping cost
    while True:        
        add_shipping = input("Do you want to add shipping cost? (yes/no): ")
        if add_shipping.lower() not in ['yes','no']:
            print("Invalid input.please enter 'yes' or 'no'.")
            continue
        if add_shipping =='yes':
            try:
                shipping_cost = float(input("Enter the shipping cost:$ "))
                if shipping_cost < 0:
                    print("Shipping cost cannot be negative.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid number for shipping cost.")
                continue
        else:
            shipping_cost = 0.00
        break
    
    #calculating VAT and total Price    
    vat_amount = total_price * VAT_RATE
    total_price += shipping_cost + vat_amount
    
    #Generating the invoice
    generate_invoice_2(transaction1,customer_name, total_price, shipping_cost,vat_amount,phone_number,address)



def generate_invoice_2(transaction1,customer_name, total_price, shipping_cost,vat_amount,phone_number,address):
    """
        Generating a details invoice for the sale
        -Include the list of purchased items with their detais
        -Adds customer name, date and time of purchase, VAT and sipping cost.
        -save and print the invoice.
    """
    invoice_text = f""" INVOICE :
==============================================================================================
                                    BRJ Furniture Store    
                                         INVOICE    
==============================================================================================

Customer Details:
----------------------------------------------------------------------------------------------
Name: {customer_name}
Phone Number: {phone_number}
Address: {address}
Date and Time of Purchase: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==============================================================================================

Purchased Items:
----------------------------------------------------------------------------------------------
| No | Furniture ID |     Manufacturer Name        |  Product Name  |  Quantity  |    Price |
----------------------------------------------------------------------------------------------
"""
    count = 1
    for transaction in transaction1:
        invoice_text += f"| {count:<3} | {transaction['furniture_id']:<11} | {transaction['manufacturer_name']:<28} | {transaction['name']:<14} | {transaction['quantity']:<10} | ${transaction['price']:<6} |\n"
        count += 1

    invoice_text += """----------------------------------------------------------------------------------------------
"""

    invoice_text += f"""
----------------------------------------------------------------------------------------------
SubTotal:                       ${total_price - vat_amount - shipping_cost:.2f}
VAT (13%):                      ${vat_amount:.2f}
Shipping Cost:                  ${shipping_cost:.2f}
----------------------------------------------------------------------------------------------
Total Amount:                   ${total_price:.2f}
==============================================================================================

                               THANK YOU FOR SHOPPING WITH US!
==============================================================================================
"""
    # printing the invoice in terminal 
    print(invoice_text)
    
    #Saving the invoice to a text file
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + "_" + "sales" + "_invoice.txt"
    with open(filename, "w") as file:
        file.write(invoice_text)
        print("Transactions Successfully Conducted.")
