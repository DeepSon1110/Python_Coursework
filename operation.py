def calculate_price(price_per_item, quantity):
    """
    Calculate the total price of items based on the price per item and the quantity.

    Args:
        price_per_item (str): the price of a single items
        quantity (_type_): the quantity of the items

    Returns:
        floats: the total price by calculating the price per items and quantity
    """ 
    
    #removing dollar sign and commas and convert price string to float
    price_per_item = float(price_per_item.replace('$', '').replace(',', ''))
    
    #multiplying the price per item by the quantity to get the total price
    return price_per_item * quantity
