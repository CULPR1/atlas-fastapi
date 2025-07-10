from config.init import inv,profile,trans,client


def dict_inv(itemname : str,number_of_units : int,price_of_unit : float,seller_id : str):
    return {
        "itemname" : itemname,
        "Number of Units" : number_of_units,
        "Price of one" : price_of_unit,
        "seller_id" : seller_id,
    }


def addInventory(itemname : str,number_of_units : int,price_of_unit : float,seller_id : str):
    
    try:
        result = inv.insert_one(dict_inv(itemname,number_of_units,price_of_unit,seller_id))
        if result.inserted_id:
            return f"Item {itemname} successfully added"
        else:
            return "something went wrong"

    except Exceptions as e:
        return f"Error : {str(e)}"



def deleteInventory(itemname : str,seller_id : str):
    try:
        res_find = inv.count_documents({"itemname" : itemname, "seller_id" : seller_id})
        if res_find > 0:
            result = inv.delete_one({"itemname" : itemname, "seller_id" : seller_id})
            if result.deleted_count > 0:
                return f"Item {itemname} successfully deleted"
            else: 
                return "Something went wrong"
        else:
            return f"Item {itemname} not in {seller_id}'s Inventory"
    except Exception as e:
        return f"Error : {str(e)}"


def updateInventory(itemname : str,new_number : int,new_price : float,seller_id : str):
    try: 
        res = inv.update_one({"itemname" : itemname, "seller_id" : seller_id},{"$set":{"Number of Units" : new_number, "Price of one" : new_price}})
        if res.matched_count > 0:
            if res.modified_count > 0:
                return f"item {itemname} successfully updated"
            else:
                return f"There were no changes made since parameters are exactly the same"
        else:
            return f"No item of that name was found in {seller_id}'s inventory"
    except Exception as e:
        return f"Error {str(e)}"

def listInventory(seller_id):
    inv_list = list(inv.find({"seller_id" : seller_id},{"_id" : 0}))
    inv_count = inv.count_documents({"seller_id" : seller_id})
    if inv_count > 0:
        return inv_list
    else: 
        return f"There are {inv_count} items in {seller_id}'s inventory"

# Test inventory functions for seller_001
# print("\n=== Testing seller_001 Inventory ===")
# print("Add apples:", addInventory("apples", 50, 1.99, "seller_001"))
# print("Add bananas:", addInventory("bananas", 30, 0.99, "seller_001"))
# print("Add oranges:", addInventory("oranges", 40, 1.49, "seller_001"))

# print("\nList seller_001 inventory:")
# print(listInventory("seller_001"))

# print("\nUpdate apples inventory:")
# print(updateInventory("apples", 45, 2.19, "seller_001"))
# print("Try update non-existent item:")
# print(updateInventory("grapes", 10, 3.99, "seller_001"))

# print("\nDelete oranges:")
# print(deleteInventory("oranges", "seller_001"))
# print("Try delete non-existent item:")
# print(deleteInventory("mangoes", "seller_001"))

# # Test inventory functions for seller_002
# print("\n=== Testing seller_002 Inventory ===")
# print("Add laptops:", addInventory("laptops", 10, 999.99, "seller_002"))
# print("Add headphones:", addInventory("headphones", 25, 149.99, "seller_002"))
# print("Add keyboards:", addInventory("keyboards", 30, 59.99, "seller_002"))

# print("\nList seller_002 inventory:")
# print(listInventory("seller_002"))

# print("\nUpdate headphones inventory:")
# print(updateInventory("headphones", 20, 129.99, "seller_002"))

# print("\nDelete keyboards:")
# print(deleteInventory("keyboards", "seller_002"))

# # Verify final inventories
# print("\n=== Final Inventory Check ===")
# print("seller_001 inventory:")
# print(listInventory("seller_001"))
# print("\nseller_002 inventory:")
# print(listInventory("seller_002"))

# # Edge case testing
# print("\n=== Edge Case Testing ===")
# print("Add empty item name:", addInventory("", 10, 1.99, "seller_001"))
# print("Add zero price item:", addInventory("test_item", 10, 0, "seller_001"))
# print("Add negative quantity:", addInventory("test_item", -5, 1.99, "seller_001"))