# from config.init import *
# from utils.seller_functions import *
# from fastapi import FastAPI
# from pydantic import BaseModel, PositiveInt, PositiveFloat

# class Item(BaseModel):
#     itemname: str
#     number_of_units: PositiveInt
#     price_of_unit: PositiveFloat
#     seller_id: str


# class Item_rem(BaseModel):
#     itemname: str
#     seller_id: str


# app = FastAPI()

# #@app.post("/add_items", response_model = list[str], description = "items are added to the inventory, requires a list of itemname,number_of units,price_of_unit,seller_id, return a list of messages.")
# @app.post("/add_items", response_model=list[str], 

# description="""Adds items to the inventory. Supports both single item and multiple items.

# For single item, use individual parameters:
# - itemname: string - Name of item to add
# - number_of_units: integer (positive) - Number of units to add  
# - price_of_unit: float (positive) - Price per unit
# - seller_id: string - ID of seller

# For multiple items, use a list parameter:
# - items: list of Item objects, where each Item = {
#     'itemname': string,
#     'number_of_units': integer (positive),
#     'price_of_unit': float (positive),
#     'seller_id': string
#   }"""
  
#   )
# def add_items(items: Item | list[Item]):
#     # """
#     # adds items to the inventory, requires a list in the form
#     # Item  = {
#     # "itemname": "<itemname>",
#     # "number_of_units": <number_of_units>,
#     # "price_of_unit": <price_of_unit>,
#     # "seller_id": "<seller_id>"
#     # }
#     # """
#     added_items = []
#     if not isinstance(items, list[Item]):
#         items = [items]
#     for item in items:
#         result = addInventory(item.itemname, item.number_of_units, item.price_of_unit, item.seller_id)
#         added_items.append(result)
#     return added_items


# @app.delete("/delete_item", response_model = list[str], description = "items are deleted from the inventory, requires a list of itemname and seller_id, return a list of messages.")
# def delete_inv(items : Item_rem | list[Item_rem]):
#     deleted_items = []
#     if not isinstance(items, list):
#         items = [items]
#     for item in items:
#         result = deleteInventory(item.itemname,item.seller_id)
#         deleted_items.append(result)
#     return deleted_items



# @app.get("/list_inventory/{seller_id}", description = "lists all items in the inventory for a given seller_id, returns a list of items.")
# def list_inventory(seller_id: str):
#     return listInventory(seller_id)



# @app.put("/update_item", response_model = list[str], description = "updates items in the inventory, requires a list of itemname,number_of_units,price_of_unit,seller_id, return a list of messages.")
# def update_item(items: Item | list[Item]):
#     updated_items = []
#     if not isinstance(items, list):
#         items = [items]
#     for item in items:
#         result = updateInventory(item.itemname, item.number_of_units, item.price_of_unit, item.seller_id)
#         updated_items.append(result)
#     return updated_items


from config.init import *
from utils.seller_functions import *
from fastapi import FastAPI, Query, Body

app = FastAPI()

@app.post(
    "/add_items",
    response_model=list[str],
    description="Adds items to inventory (single or multiple)"
)
def add_items(
    itemname: str = Body(...),
    number_of_units: int = Body(..., gt=0),
    price_of_unit: float = Body(..., gt=0),
    seller_id: str = Body(...),
    items: list[dict] = Body(None)
):
    added_items = []
    if items:
        # Handle multiple items
        for item in items:
            result = addInventory(
                item['itemname'],
                item['number_of_units'],
                item['price_of_unit'],
                item['seller_id']
            )
            added_items.append(result)
    else:
        # Handle single item
        result = addInventory(itemname, number_of_units, price_of_unit, seller_id)
        added_items.append(result)
    return added_items

@app.post(
    "/delete_item",
    response_model=list[str],
    description="Deletes items from inventory"
)
def delete_inv(
    itemname: str = Body(None),
    seller_id: str = Body(None),
    items: list[dict] = Body(None)
):
    deleted_items = []
    if items:
        # Handle multiple items
        for item in items:
            result = deleteInventory(item['itemname'], item['seller_id'])
            deleted_items.append(result)
    else:
        # Handle single item
        result = deleteInventory(itemname, seller_id)
        deleted_items.append(result)
    return deleted_items

@app.get(
    "/list_inventory/{seller_id}",
    description="Lists all items for a seller"
)
def list_inventory(seller_id: str):
    return listInventory(seller_id)

@app.put(
    "/update_item",
    response_model=list[str],
    description="Updates items in inventory"
)
def update_item(
    itemname: str = Body(...),
    number_of_units: int = Body(..., gt=0),
    price_of_unit: float = Body(..., gt=0),
    seller_id: str = Body(...),
    items: list[dict] = Body(None)
):
    updated_items = []
    if items:
        # Handle multiple items
        for item in items:
            result = updateInventory(
                item['itemname'],
                item['number_of_units'],
                item['price_of_unit'],
                item['seller_id']
            )
            updated_items.append(result)
    else:
        # Handle single item
        result = updateInventory(itemname, number_of_units, price_of_unit, seller_id)
        updated_items.append(result)
    return updated_items