from config.init import *
from utils.seller_functions import *
import json 
from fastapi import FastAPI
from pydantic import BaseModel, PositiveInt, PositiveFloat

class Item(BaseModel):
    itemname: str
    number_of_units: PositiveInt
    price_of_unit: PositiveFloat
    seller_id: str


class Item_rem(BaseModel):
    itemname: str
    seller_id: str

class Item_rem_request(BaseModel):
    item_rem_request : list[Item_rem]

class Itemrequest(BaseModel):
    item_list : list[Item]


app = FastAPI()

#@app.post("/add_items", response_model = list[str], description = "items are added to the inventory, requires a list of itemname,number_of units,price_of_unit,seller_id, return a list of messages.")
@app.post("/add_items", response_model=list[str], 

description="""Adds items to the inventory. Supports both single item and multiple items.

For single item, use individual parameters:
- itemname: string - Name of item to add
- number_of_units: integer (positive) - Number of units to add  
- price_of_unit: float (positive) - Price per unit
- seller_id: string - ID of seller

For multiple items, use a list parameter:
- items: list of Item objects, where each Item = {
    'itemname': string,
    'number_of_units': integer (positive),
    'price_of_unit': float (positive),
    'seller_id': string
  }"""
  
  )
def add_items(request: Item | Itemrequest):
    # """
    # adds items to the inventory, requires a list in the form
    # Item  = {
    # "itemname": "<itemname>",
    # "number_of_units": <number_of_units>,
    # "price_of_unit": <price_of_unit>,
    # "seller_id": "<seller_id>"
    # }
    # """
    added_items = []
    if not isinstance(request, Itemrequest):
        items = [request]
    else:
        items = request.item_list
    for item in items:
        result = addInventory(item.itemname, item.number_of_units, item.price_of_unit, item.seller_id)
        added_items.append(result)
    return added_items


@app.delete("/delete_item", response_model = list[str], description = "items are deleted from the inventory, requires a list of itemname and seller_id, return a list of messages.")
def delete_inv(request : Item_rem | Item_rem_request):
    deleted_items = []
    if isinstance(request, Item_rem_request):
        items = request.item_rem_request
    else:
        items = [request]
    for item in items:
        result = deleteInventory(item.itemname,item.seller_id)
        deleted_items.append(result)
    return deleted_items



@app.get("/list_inventory/{seller_id}", description = "lists all items in the inventory for a given seller_id, returns a list of items.")
def list_inventory(seller_id: str):
    return listInventory(seller_id)


@app.put("/update_item", response_model = list[str], description = "updates items in the inventory, requires a list of itemname,number_of_units,price_of_unit,seller_id, return a list of messages.")
def update_item(request: Itemrequest | Item):
    updated_items = []
    if isinstance(request,Itemrequest):
        items = request.item_list

    else:
        items = [request]
    for item in items:
        result = updateInventory(item.itemname, item.number_of_units, item.price_of_unit, item.seller_id)
        updated_items.append(result)
    return updated_items