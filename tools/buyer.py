from utils.buyer_functions import *
from config.init import *
from pydantic import BaseModel,PositiveInt, PositiveFloat
from fastapi import FastAPI


app = FastAPI()


class Searchrequest(BaseModel):
    item_name : str = None
    seller_id : str = None



class Cartrequest(BaseModel):
    itemname : str
    number_of_units : PositiveInt
    price : PositiveFloat
    seller_id : str
    buyer_id : str


class listCartrequest(BaseModel):
    list : list[Cartrequest]

class Balance(BaseModel):
    buyer_id : str
    balance : float


class removerequest(BaseModel):
    item_name : str = None
    buyer_id : str

class listremoverequest(BaseModel):
    list : list[removerequest]


class Payment(BaseModel):
    buyer_id : str
    payment_amount : PositiveFloat = None




@app.post(
    "/buyer/search_shop",
    name = "search_shop" , 
    response_model = list[dict] | str,
    description = """A tool to allow a buyer to search for items in the store, 
    the inputs can be just the itemname, the seller name, both or none which will give the entire list
    """)


def search_shop(query = Searchrequest):
    return searchShop(query.item_name,query.seller_id)



@app.post(
    "/buyer/addtoCart",
    name = "add_to_cart",
    response_model = list[str],
    description = """ add one item or a list of items to the buyer's profile so that it can be referenced when payment is required
    """)


def add_to_cart(items = Cartrequest | listCartrequest):
    if not isinstance(items,listCartrequest) :
        items = [items]
    results = []
    for item in items:
        response = addtoCart(item.itemname,item.number_of_units,item.price,item.seller_id,item.buyer_id)
        results.append(response)

    return results


@app.post(
    "/buyer/addBalance",
    name = "addBalance",
    response_model = str,
    description = """ adds the balance section to the buyer's profile so that
    the buyer can use the balance to pay for his purchase rather than his own payment"""
    )

def addBalance(balance_req = Balance):
    return add_balance(balance_req.buyer_id,balance_req.balance)




@app.post(
    "/buyer/updateBalance",
    name = "updateBalance",
    response_model = str,
    description = """ updates the balance section to the buyer's profile, if the balance is to be withdrawn the value of balance input should be negative"""
    )

def updateBalance(balance_req = Balance):
    return add_balance(balance_req.buyer_id,balance_req.balance)



@app.post(
    "/buyer/removeCart",
    name = "removeCart",
    response_model = list[str],
    description = """ removes the items in the cart when mentioned, can be a single item or  a list of items"""
    )

def addBalance(remove_req = removerequest | listremoverequest):

    if not isinstance(remove_req,listremoverequest):
        remove_req = [remove_req]
    response = []
    for item in remove_req:
        response = remove_from_cart(item.item_name,item.buyer_id)

    return response


@app.get(
    "/buyer/Total_cost",
    name = "Total_cost",
    response_model = float | str,
    description = "gives the buyer a total cost of all the items in his cart if cart exsists, or returns that ther is nothing in cart")


def Total_cost(buyer_id : str):
    return Totalcost(buyer_id)




@app.post(
    "/buyer/payment",
    name = "payment",
    description = "allows the buyer to pay for the items in his cart, one can pay using cash provided or the balance account under their name, if the balance account is to be used the payment field is set to None"
)

def payment(pay_req = Payment):
    return pay(pay_req.buyer_id,pay_req.payment_amount)



@app.get(
    "/buyer/view_cart",
    name = "Viewcart",
    description = "allows the buyer to see all the items in his cart"
)

def Viewcart(buyer_id : str):
    return view_cart(buyer_id)
    


    





