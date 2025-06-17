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





