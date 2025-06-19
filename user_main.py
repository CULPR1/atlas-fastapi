from tools.user import *
from fastapi_mcp import FastApiMCP

mcp = FastApiMCP(app, name= "user_server", description="user server for registering and logging in.")


mcp.mount()

# if __name__ == "__main__":
#     import uvicorn

#uvicorn.run("user_main:app", host="0.0.0.0", port=8000, reload=True)