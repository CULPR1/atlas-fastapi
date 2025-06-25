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


def addtoCart (itemname : str,number_of_units : int, price_of_unit : float ,seller_id : str,buyer_id : str):
    with client.start_session() as session:
        try:
            cart = []
            if inv.count_documents({"seller_id" : seller_id,"itemname" : itemname}) > 0:
                found_item = list(inv.find({"seller_id" : seller_id,"itemname" : itemname}))
                if number_of_units <= found_item[0]["Number of Units"]:

                        cart_item = {
                            "itemname" : found_item[0]["itemname"],
                            "Number of Units" : number_of_units,
                            "Price of one" : found_item[0]["Price of one"],
                            "Total cost" : found_item[0]["Price of one"] * float(number_of_units),
                            "seller_id" : seller_id,
                            "buyer_id" : buyer_id
                        }

                        cart.append(cart_item)

                else:
                    print(f"Number of {str(itemname)} exceeds amount in stock")

            if not cart:
                return "No changes to cart"
            else:
                operate = profile.update_one({"user_id" : buyer_id},{"$push":{"cart" : {"$each" : cart}}},session=session)
                if operate.matched_count > 0:
                    if operate.modified_count > 0:
                        return f"added {cart}to cart successfully"
                    else :
                        return "some descrepancies occured"

                else:
                    return "some issue with buyer_id"

            session.commit_transaction()
        except Exception as e:
            print( f"Error : {str(e)}")
            session.abort_transaction

def start_balance(buyer_id : str, balance : float): #works
    with client.start_session() as session:
        try:
            if profile.count_documents({"user_id" : buyer_id}) == 1:
                operate = profile.update_one({"user_id" : buyer_id},{"$set":{"balance" : balance}},session=session)
                if operate.matched_count > 0:
                    if operate.modified_count > 0:
                        return f"added {balance}to balance successfully"
                    else :
                        return "some descrepancies occured"

                else:
                    return "some issue with buyer_id"
            client.commit_session()
        except Exception as e:
            return (f"Error {str(e)}")
            client.abort_transaction()


def add_balance(buyer_id : str, balance : float): 
    with client.start_session() as session:
        try:
            if profile.count_documents({"user_id" : buyer_id}) == 1:
                operate = profile.update_one({"user_id" : buyer_id},{"$push":{"balance" : balance}},session=session)
                if operate.matched_count > 0:
                    if operate.modified_count > 0:
                        return f"added {balance}to balance successfully"
                    else :
                        return "some descrepancies occured"

                else:
                    return "some issue with buyer_id"
            client.commit_session()
        except Exception as e:
            return (f"Error {str(e)}")
            client.abort_transaction()



def update_balance(buyer_id : str, balance : float):
    with client.start_session() as session:
        try:
            if profile.count_documents({"user_id" : buyer_id}) == 1:
                operate = profile.update_one({"user_id" : buyer_id},{"$inc":{"balance" : balance}},session=session)
                if operate.matched_count > 0:
                    if operate.modified_count > 0:
                        return f"increased balance by {balance}"
                    else :
                        return "some descrepancies occured"

                else:
                    return "some issue with buyer_id"
            client.commit_session()
        except Exception as e:
            return (f"Error {str(e)}")
            client.abort_transaction()




def remove_from_cart(itemname : str, buyer_id : str):
    with client.start_session() as session:
        try:
            res = profile.update_one({"user_id" : buyer_id},{"$pull":{"cart":{"itemname" : itemname}}},session=session)
            if res.matched_count > 0:
                if res.modified_count > 0:
                    return f"removed {itemname} from cart"
                else :
                    return "nothing removed"

            else:
                return "buyer_id issue"
            client.commit_transaction()
        except Exception as e:
            return (f"Error {str(e)}")
            client.abort_transaction()

                
def Totalcost(buyer_id : str):
    buyer_profile = list(profile.find({"user_id" : buyer_id}))[0]
    cost = 0.0
    for i in buyer_profile["cart"]:
        cost += i["Total cost"]

    return cost

#print(Totalcost("jack_234"))




def pay(buyer_id : str, payment_amount : float | None=None):
    if payment_amount is None:
        with client.start_session() as session:
            try:
                buyer_profile = list(profile.find({"user_id" : buyer_id}))[0]
                total_cost = Totalcost(buyer_id)
                if buyer_profile["balance"] >= total_cost:
                    insert = []
                    for i in buyer_profile["cart"]:
                        insert = {
                            "buyer_id" : buyer_id,
                            "seller_id" : i["seller_id"],
                            "itemname" : i["itemname"],
                            "cost" : i["Total cost"]
                        }

                        result = trans.insert_one(insert,session=session)
                        result_2 = inv.update_one({"itemname" : i["itemname"], "seller_id" : i["seller_id"]},{"$inc":{"Number of Units" : -i["Number of Units"]}},session=session)
                        result_3 = profile.update_one({"user_id" : buyer_id},{"$pull":{"cart":{"itemname" : i["itemname"]}}},session=session)
                        result_4 = profile.update_one({"user_id" : buyer_id},{"$inc":{"balance": -i ["Total cost"]}},session=session)

                    return "successfully paid"

                else:
                    return "not enough money in account"
                session.commit_transaction()


            except Exception as e :
                return f"Error {str(e)}"
                session.abort_transaction()


    else:
        with client.start_session() as session:
            try:
                buyer_profile = list(profile.find({"user_id" : buyer_id}))[0]
                total_cost = Totalcost(buyer_id)
                if payment_amount >= total_cost:
                    insert = []
                    for i in buyer_profile["cart"]:
                        insert = {
                            "buyer_id" : buyer_id,
                            "seller_id" : i["seller_id"],
                            "itemname" : i["itemname"],
                            "cost" : i["Total cost"]
                        }

                        result = trans.insert_one(insert,session=session)
                        result_2 = inv.update_one({"itemname" : i["itemname"], "seller_id" : i["seller_id"]},{"$inc":{"Number of Units" : -i["Number of Units"]}},session=session)
                        result_3 = profile.update_one({"user_id" : buyer_id},{"$pull":{"cart":{"itemname" : i["itemname"]}}},session=session)

                    remaining = payment_amount - total_cost

                    return "successfully paid", remaining

                else:
                    return "payment amount is lesser than total cost"
                session.commit_transaction()


            except Exception as e :
                return f"Error {str(e)}"
                session.abort_transaction()



def view_cart(buyer_id : str ):
    cart = list(profile.find({"user_id" : buyer_id},{"_id" : 0}))[0]["cart"]
    return cart

    