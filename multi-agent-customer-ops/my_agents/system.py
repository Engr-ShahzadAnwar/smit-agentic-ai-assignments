# from agents import Agent, function_tool
# from my_agents.tools import *
# from utils.gemini import model

# context_tool = function_tool(get_user_context)
# sales_tool = function_tool(search_products)
# support_tool = function_tool(handle_support)
# orders_tool = function_tool(get_order_status)

# # MODEL_NAME = "gemini-2.5-flash"

# context_agent = Agent(
#     name="Context_Agent",
#     model=model,
#     instructions="Retrieve user history and context.",
#     tools=[context_tool]
# )

# support_agent = Agent(
#     name="Support_Agent",
#     model=model,
#     instructions="Solve complaints professionally.",
#     tools=[support_tool]
# )

# sales_agent = Agent(
#     name="Sales_Agent",
#     model=model,
#     instructions="Handle buying intent and recommend products.",
#     tools=[sales_tool]
# )

# orders_agent = Agent(
#     name="Orders_Agent",
#     model=model,
#     instructions="Check order status.",
#     tools=[orders_tool]
# )

# router_agent = Agent(
#     name="Router_Agent",
#     model=model,
#     instructions="""
# Route request intelligently:

# complaint/refund/late -> Support_Agent
# buy/product/price -> Sales_Agent
# order/status -> Orders_Agent
# else -> Context_Agent
# """,
#     handoffs=[
#         support_agent,
#         sales_agent,
#         orders_agent,
#         context_agent
#     ]
# )






#--------------------------------------------------------------------
# from my_agents.tools import (
#     get_user_context,
#     search_products,
#     handle_support,
#     get_order_status
# )

# def run_multi_agent(msg):

#     text = msg.lower()

#     outputs = []

#     # Router Logic
#     if "buy" in text or "price" in text:
#         outputs.append(search_products(msg))

#     elif "refund" in text or "late" in text or "issue" in text:
#         outputs.append(handle_support(msg))

#     elif "order" in text:
#         outputs.append(get_order_status(10))

#     else:
#         outputs.append(get_user_context(10))

#     return "\n".join(map(str, outputs))



#----------------------------------------------------------------------

from agents import Agent, function_tool
from my_agents.tools import (
    get_user_context,
    get_all_users,
    search_products,
    get_all_products,
    get_product_by_brand,
    handle_support,
    get_order_status,
    get_order_by_id,
    update_order_status
)

from utils.gemini import model

# ==================================================
# TOOLS
# ==================================================

context_tool = function_tool(get_user_context)
users_tool = function_tool(get_all_users)

sales_tool = function_tool(search_products)
products_tool = function_tool(get_all_products)
brand_tool = function_tool(get_product_by_brand)

support_tool = function_tool(handle_support)

orders_tool = function_tool(get_order_status)
single_order_tool = function_tool(get_order_by_id)
update_order_tool = function_tool(update_order_status)

# ==================================================
# AGENTS
# ==================================================

context_agent = Agent(
    name="Context_Agent",
    model=model,
    instructions="""
Retrieve customer profile, history and user context.
""",
    tools=[context_tool, users_tool]
)

sales_agent = Agent(
    name="Sales_Agent",
    model=model,
    instructions="""
Handle buying intent.
Recommend Pakistani clothing products.
""",
    tools=[sales_tool, products_tool, brand_tool]
)

support_agent = Agent(
    name="Support_Agent",
    model=model,
    instructions="""
Handle complaints professionally.
Solve refund / late parcel / damaged order issues.
""",
    tools=[support_tool]
)

orders_agent = Agent(
    name="Orders_Agent",
    model=model,
    instructions="""
Track orders.
Check order status.
Update order if requested.
""",
    tools=[
        orders_tool,
        single_order_tool,
        update_order_tool
    ]
)

router_agent = Agent(
    name="Router_Agent",
    model=model,
    instructions="""
You are smart router.

Route request:

complaint / refund / damaged / late
-> Support_Agent

buy / product / price / clothes / shirt / jeans
-> Sales_Agent

order / tracking / status / cancel / delivered
-> Orders_Agent

user / profile / history
-> Context_Agent
""",
    handoffs=[
        support_agent,
        sales_agent,
        orders_agent,
        context_agent
    ]
)