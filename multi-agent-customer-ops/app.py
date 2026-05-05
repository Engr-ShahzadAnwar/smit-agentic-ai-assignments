# from fastapi import FastAPI
# from pydantic import BaseModel
# from agents import Runner
# from my_agents.system import router_agent

# app = FastAPI()

# class ChatRequest(BaseModel):
#     message: str

# @app.post("/chat")
# async def chat(req: ChatRequest):
#     result = await Runner.run(
#         router_agent,
#         req.message
#     )

#     return {
#         "response": result.final_output
#     }


# from fastapi import FastAPI
# from pydantic import BaseModel

# from my_agents.system import run_multi_agent

# app = FastAPI()

# class ChatRequest(BaseModel):
#     message:str

# @app.post("/chat")
# async def chat(req: ChatRequest):

#     result = run_multi_agent(req.message)

#     return {
#         "response": result
#     }




from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import Runner

from my_agents.system import router_agent
from my_agents.tools import (
    get_all_users,
    get_all_products,
    get_order_status,
    update_order_status
)

app = FastAPI(
    title="AI Multi-Agent Customer Ops API",
    version="1.0.0",
    description="Gemini Powered + OpenAI Agents SDK"
)

# ==================================================
# REQUEST MODELS
# ==================================================

class ChatRequest(BaseModel):
    message: str


class OrderUpdateRequest(BaseModel):
    order_id: int
    status: str


# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():
    return {
        "message": "AI Multi-Agent Customer Ops Running"
    }


# ==================================================
# AI CHAT ENDPOINT
# ==================================================

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        result = await Runner.run(
            router_agent,
            req.message
        )

        return {
            "success": True,
            "response": result.final_output
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==================================================
# USERS
# ==================================================

@app.get("/users")
def users():
    return {
        "success": True,
        "data": get_all_users()
    }


# ==================================================
# PRODUCTS
# ==================================================

@app.get("/products")
def products():
    return {
        "success": True,
        "data": get_all_products()
    }


# ==================================================
# ORDERS BY USER
# ==================================================

@app.get("/orders/{user_id}")
def orders(user_id: int):
    return {
        "success": True,
        "data": get_order_status(user_id)
    }


# ==================================================
# UPDATE ORDER
# ==================================================

@app.put("/orders/update")
def order_update(req: OrderUpdateRequest):
    return {
        "success": True,
        "data": update_order_status(
            req.order_id,
            req.status
        )
    }