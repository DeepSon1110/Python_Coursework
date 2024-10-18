def read_file():
    """
    This function read the furniture items from a tetx file i.e (Furniture.txt).
    
    Returns:
        list : A list of dictionaries, where each dictionary represents a furniture items with keys:
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        furniture_list = []
        
        #open the file 
        with open("Furniture.txt", "r") as file:
            for line in file:
                #split each line based on comma and space
                values = line.strip().split(", ")
                #creating dictionary for each items and add it to the list
                furniture_list.append(
                    {
                    "furniture_id":values[0],
                    "manufacturer_name":values[1],
                    "name":values[2],
                    "quantity":values[3],
                    "price":values[4]       
                    }
                )

            return furniture_list
    except FileNotFoundError:
        #handling exception if file not found
        print("File not found.")
        
def display_available_furniture(furniture_list):
    """
    Display Available Furnitures
    
    Args : 
        furniture_list (list) : A list of dictionaries, where each dictionary represents a furniture items.
    """
    
    furniture_list = read_file()
    print("---------------------------------------------------------------------------------------------------------------------------------")
    print("|    Furniture id     |         Manufacturer Name      |     Product Name     |   Quantity Available  |    price per product   | ")
    print("---------------------------------------------------------------------------------------------------------------------------------")
    
    #Iterating over the list and displaying them
    for values in furniture_list:
        #displays items with non-negative values
        if int(values["quantity"]) >= 0:
            furniture_id=int(values["furniture_id"])
            manufacturer_name=values["manufacturer_name"]
            name=values["name"]
            quantity=int(values["quantity"])
            price=float(values["price"].strip('$'))
            
            #printing each row
            print(f"|{furniture_id: <20} | {manufacturer_name: <30} | {name: <20} | {quantity: <22}| ${price: <21.2f} |" )
    
    #footer of the table   
    print("---------------------------------------------------------------------------------------------------------------------------------")
   
    

            
            