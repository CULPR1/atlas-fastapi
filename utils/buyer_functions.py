from pydantic import BaseModel,PositiveInt, PositiveFloat
from config.init import profile,trans,inv,client




def dict_cart(itemname : str,item_number : int,item_price : float,seller_id :str):
    return{
        "itemname" : itemname,
        "item_number" : item_number,
        "item_price" : item_price,
        "seller_id" : seller_id
    }






def searchShop(itemname :str | None=None, seller_id : str | None=None):
    try:
        if itemname is None and seller_id is None:
            res_1 = list(inv.find({},{"_id" : 0}))
            return res_1
        elif itemname is None:
            res_2 = list(inv.find({"seller_id" : seller_id},{"_id" : 0}))
            return res_2
        elif seller_id is None:
            res_3 = list(inv.find({"itemname" : itemname},{"_id" : 0}))
            return res_3
        else : 
            res_4 = list(inv.find({"seller_id" : seller_id,"itemname" : itemname},{"_id" : 0}))
            return res_4

    except Exception as e:
        return f"Error : {str(e)}"



# item_ls = [{"seller_id" : "mark_123", "itemname" : "apple", "quantity" : 3},{"seller_id" : "mark_123", "itemname" : "banana", "quantity" : 3},{"seller_id" : "mark_123", "itemname" : "pineapple", "quantity" : 1}]
# print(item_ls[0]["seller_id"])




# def addtoCart (itemname : str,number_of_units : int, price_of_unit : float ,seller_id : str,buyer_id : str):
#     with client.start_session() as session:
#         try:
#             cart = []
#             if inv.count_documents({"seller_id" : seller_id,"itemname" : itemname}) > 0:
#                 found_item = list(inv.find({"seller_id" : seller_id,"itemname" : itemname}))
#                 if number_of_units <= found_item[0]["Number of Units"]:

#                         cart_item = {
#                             "itemname" : found_item[0]["itemname"],
#                             "Number of Units" : number_of_units,
#                             "Price of one" : found_item[0]["Price of one"],
#                             "Total cost" : found_item[0]["Price of one"] * float(number_of_units),
#                             "seller_id" : seller_id,
#                             "buyer_id" : buyer_id
#                         }

#                         cart.append(cart_item)

#                 else:
#                     print(f"Number of {str(itemname)} exceeds amount in stock")

#             if not cart:
#                 return "No changes to cart"
#             else:
#                 operate = profile.update_one({"user_id" : buyer_id},{"$push":{"cart" : {"$each" : cart}}},session=session)
#                 if operate.matched_count > 0:
#                     if operate.modified_count > 0:
#                         return f"added {cart}to cart successfully"
#                     else :
#                         return "some descrepancies occured"

#                 else:
#                     return "some issue with buyer_id"

#             session.commit_transaction()
#         except Exception as e:
#             print( f"Error : {str(e)}")
#             session.abort_transaction()


def addtoCart(itemname: str, number_of_units: int, price_of_unit: float, seller_id: str, buyer_id: str):
    with client.start_session() as session:
        try:
            # Check if item exists in inventory (case-sensitive exact match)
            query = {
                "seller_id": seller_id,
                "itemname": {"$regex": f"^{itemname}$", "$options": "i"},  # Case-insensitive exact match
                "Number of Units": {"$gte": number_of_units}
            }
            
            found_item = inv.find_one(query)
            
            if found_item:
                cart_item = {
                    "itemname": found_item["itemname"],
                    "Number of Units": number_of_units,
                    "Price of one": found_item["Price of one"],
                    "Total cost": found_item["Price of one"] * float(number_of_units),
                    "seller_id": seller_id,
                    "buyer_id": buyer_id
                }

                operate = profile.update_one(
                    {"user_id": buyer_id},
                    {"$push": {"cart": cart_item}},
                    session=session
                )
                
                if operate.modified_count > 0:
                    return f"Added {itemname} to cart successfully"
                return "Failed to add to cart"
            
            return f"Item not available or insufficient stock"
            
        except Exception as e:
            session.abort_transaction()
            return f"Error: {str(e)}"

# def remove_duplicates(buyer_id : str):
#     # this functions removes multiple addition of the the same item to the cart and combines them into one entry
#     with client.start_session() as session:
#         try:
#             for buyer


def update_balance(buyer_id : str, balance : float):
    with client.start_session() as session:
        try:
            if profile.count_documents({"user_id" : buyer_id}) == 1:
                operate = profile.update_one({"user_id" : buyer_id},{"$inc":{"balance" : balance}},session=session)
                final_balance = list(profile.find({"user_id" : buyer_id}))[0]["balance"]
                if operate.matched_count > 0:
                    if operate.modified_count > 0:
                        return f"increased balance by {balance}, final balance is {final_balance}"
                    else :
                        return "some descrepancies occured"

                else:
                    return "some issue with buyer_id"
            session.commit_transaction()
        except Exception as e:
            return (f"Error {str(e)}")
            client.abort_transaction()



# listing = profile.find({"user_id" : "jack_234"})
# print(listing["cart"][2]["itemname"])



# def remove_from_cart(itemname : str | None, buyer_id : str):
#     if itemname is None:
#         with client.start_session() as session:
#             try:
#                 res = profile.update_one({"user_id" : buyer_id},{"$unset":"cart"},session=session)
#                 if res.matched_count > 0:
#                     if res.modified_count > 0:
#                         return f"removed cart"
#                     else :
#                         return "nothing removed"

#                 else:
#                     return "buyer_id issue"
#                 client.commit_transaction()
#             except Exception as e:
#                 return (f"Error {str(e)}")
#                 client.abort_transaction()

#     else:
#         with client.start_session() as session:
#             try:
#                 res = profile.update_one({"user_id" : buyer_id},{"$pull":{"cart":{"itemname" : itemname}}},session=session)
#                 if res.matched_count > 0:
#                     if res.modified_count > 0:
#                         return f"removed {itemname} from cart"
#                     else :
#                         return "nothing removed"

#                 else:
#                     return "buyer_id issue"
#                 client.commit_transaction()
#             except Exception as e:
#                 return (f"Error {str(e)}")
#                 client.abort_transaction()

# Make sure Totalcost is properly defined before pay() function
def Totalcost(buyer_id: str):
    buyer_profile = profile.find_one({"user_id": buyer_id})
    if buyer_profile and "cart" in buyer_profile:
        return sum(item["Total cost"] for item in buyer_profile["cart"])
    return 0.0

# Then define pay() function after Totalcost

def remove_from_cart(itemname: str | None, buyer_id: str):
    if itemname is None:
        with client.start_session() as session:
            try:
                res = profile.update_one(
                    {"user_id": buyer_id},
                    {"$set": {"cart": []}},
                    session=session
                )
                if res.modified_count > 0:
                    return "Cart cleared successfully"
                return "No cart to clear"
            except Exception as e:
                return f"Error: {str(e)}"
    else:
        with client.start_session() as session:
            try:
                res = profile.update_one(
                    {"user_id": buyer_id},
                    {"$pull": {"cart": {"itemname": itemname}}},
                    session=session
                )
                if res.modified_count > 0:
                    return f"Removed {itemname} from cart"
                return "Item not found in cart"
            except Exception as e:
                return f"Error: {str(e)}"

#print(Totalcost("jack_234"))




def pay(buyer_id: str, payment_amount: float | None = None):
    with client.start_session() as session:
        try:
            buyer_profile = profile.find_one({"user_id": buyer_id})
            if not buyer_profile:
                return "Buyer not found"
                
            total_cost = Totalcost(buyer_id)
            
            # Validate payment
            if payment_amount is None:
                if buyer_profile.get("balance", 0) < total_cost:
                    return "Insufficient funds in account"
            else:
                if payment_amount < total_cost:
                    return "Payment amount less than total cost"
            
            # Process payment
            for item in buyer_profile.get("cart", []):
                trans.insert_one({
                    "buyer_id": buyer_id,
                    "seller_id": item["seller_id"],
                    "itemname": item["itemname"],
                    "cost": item["Total cost"]
                }, session=session)
                
                inv.update_one(
                    {"itemname": item["itemname"], "seller_id": item["seller_id"]},
                    {"$inc": {"Number of Units": -item["Number of Units"]}},
                    session=session
                )
            
            # Clear cart and update balance
            profile.update_one(
                {"user_id": buyer_id},
                {"$set": {"cart": []}},
                session=session
            )
            
            balance_update = -total_cost if payment_amount is None else (payment_amount - total_cost)
            profile.update_one(
                {"user_id": buyer_id},
                {"$inc": {"balance": balance_update}},
                session=session
            )
            
            return "Payment successful" + (f", change: {balance_update}" if balance_update > 0 else "")
            
        except Exception as e:
            session.abort_transaction()
            return f"Payment failed: {str(e)}"


def view_cart(buyer_id : str ):
    if profile.find_one({"user_id" : buyer_id, "cart": {"$exists": True}}):
        try:
            cart = list(profile.find({"user_id" : buyer_id},{"_id" : 0}))[0]["cart"]
            if profile.count_documents({"user_id" : buyer_id}) > 0:
                return cart
            else : 
                return []

        except Exception as e:
            return f"Error accessing database {e}"

    else:
        return "no cart is found"

