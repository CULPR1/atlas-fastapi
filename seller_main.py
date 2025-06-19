from tools.seller import *
from fastapi_mcp import FastApiMCP

mcp = FastApiMCP(app, name= "seller_server", description="Seller server for managing inventory and seller operations.")


mcp.mount()

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("seller_main:app", host="0.0.0.0", port=8001, reload=True)
