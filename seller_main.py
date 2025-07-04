from tools.seller import *
from fastapi_mcp import FastApiMCP

mcp = FastApiMCP(app, name= "seller_server", description="Seller server for managing inventory and seller operations.")


mcp.mount()

