from tools.user import *
from fastapi_mcp import FastApiMCP

mcp = FastApiMCP(app, name= "user_server", description="user server for registering and logging in.")


mcp.mount()

