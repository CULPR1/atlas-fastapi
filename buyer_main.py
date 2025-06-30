from tools.buyer import *
from fastapi_mcp import FastApiMCP

mcp = FastApiMCP(app, name= "buyer_server", description="Seller server for managing inventory and seller operations.")


mcp.mount()

