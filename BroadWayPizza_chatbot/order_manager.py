"""
Order Management System for Broadway Pizza
Handles order creation, modification, cancellation, and tracking
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class OrderManager:
    def __init__(self):
        self.current_order = {
            "order_id": None,
            "items": [],
            "subtotal": 0,
            "delivery_fee": 150,
            "tax": 0,
            "total": 0,
            "status": "pending",
            "created_at": None
        }
        self.order_counter = 1000
    
    def create_new_order(self) -> str:
        """Initialize a new order"""
        self.order_counter += 1
        self.current_order = {
            "order_id": f"BP{self.order_counter}",
            "items": [],
            "subtotal": 0,
            "delivery_fee": 150,
            "tax": 0,
            "total": 0,
            "status": "pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return self.current_order["order_id"]
    
    def add_item(self, item_name: str, price: float, quantity: int = 1, 
                 customizations: Optional[Dict] = None) -> Dict:
        """Add an item to the current order"""
        if not self.current_order["order_id"]:
            self.create_new_order()
        
        item = {
            "name": item_name,
            "price": price,
            "quantity": quantity,
            "customizations": customizations or {},
            "item_total": price * quantity
        }
        
        # Add customization costs (e.g., stuffed crust)
        if customizations:
            for custom, cost in customizations.items():
                if isinstance(cost, (int, float)):
                    item["item_total"] += cost * quantity
        
        self.current_order["items"].append(item)
        self._calculate_totals()
        return item
    
    def remove_item(self, item_index: int) -> bool:
        """Remove an item from the order by index"""
        if 0 <= item_index < len(self.current_order["items"]):
            self.current_order["items"].pop(item_index)
            self._calculate_totals()
            return True
        return False
    
    def update_item_quantity(self, item_index: int, new_quantity: int) -> bool:
        """Update the quantity of an item"""
        if 0 <= item_index < len(self.current_order["items"]) and new_quantity > 0:
            item = self.current_order["items"][item_index]
            item["quantity"] = new_quantity
            item["item_total"] = item["price"] * new_quantity
            
            # Recalculate with customizations
            if item["customizations"]:
                for custom, cost in item["customizations"].items():
                    if isinstance(cost, (int, float)):
                        item["item_total"] += cost * new_quantity
            
            self._calculate_totals()
            return True
        return False
    
    def _calculate_totals(self):
        """Calculate order totals"""
        self.current_order["subtotal"] = sum(
            item["item_total"] for item in self.current_order["items"]
        )
        
        # Tax calculation (5% GST)
        self.current_order["tax"] = round(self.current_order["subtotal"] * 0.05, 2)
        
        # Total = Subtotal + Tax + Delivery Fee
        self.current_order["total"] = (
            self.current_order["subtotal"] + 
            self.current_order["tax"] + 
            self.current_order["delivery_fee"]
        )
    
    def get_order_summary(self) -> str:
        """Generate a formatted order summary"""
        if not self.current_order["items"]:
            return "Your cart is empty."
        
        summary = f"**Order #{self.current_order['order_id']}**\n\n"
        summary += "**Items:**\n"
        
        for idx, item in enumerate(self.current_order["items"], 1):
            summary += f"{idx}. {item['name']}"
            if item['customizations']:
                customs = ", ".join(f"{k}: {v}" for k, v in item['customizations'].items())
                summary += f" ({customs})"
            summary += f" x{item['quantity']} - Rs. {item['item_total']}\n"
        
        summary += f"\n**Subtotal:** Rs. {self.current_order['subtotal']}\n"
        summary += f"**Tax (5%):** Rs. {self.current_order['tax']}\n"
        summary += f"**Delivery Fee:** Rs. {self.current_order['delivery_fee']}\n"
        summary += f"**Total:** Rs. {self.current_order['total']}\n"
        
        return summary
    
    def confirm_order(self) -> Dict:
        """Confirm the current order"""
        if not self.current_order["items"]:
            return {"success": False, "message": "Cannot confirm empty order"}
        
        self.current_order["status"] = "confirmed"
        return {
            "success": True,
            "order_id": self.current_order["order_id"],
            "total": self.current_order["total"],
            "message": f"Order #{self.current_order['order_id']} confirmed! Total: Rs. {self.current_order['total']}"
        }
    
    def cancel_order(self) -> Dict:
        """Cancel the current order"""
        if not self.current_order["order_id"]:
            return {"success": False, "message": "No active order to cancel"}
        
        order_id = self.current_order["order_id"]
        self.current_order = {
            "order_id": None,
            "items": [],
            "subtotal": 0,
            "delivery_fee": 150,
            "tax": 0,
            "total": 0,
            "status": "cancelled",
            "created_at": None
        }
        return {
            "success": True,
            "message": f"Order #{order_id} has been cancelled"
        }
    
    def get_current_order(self) -> Dict:
        """Get the current order details"""
        return self.current_order
    
    def has_items(self) -> bool:
        """Check if current order has items"""
        return len(self.current_order["items"]) > 0
    
    def get_item_count(self) -> int:
        """Get total number of items in order"""
        return sum(item["quantity"] for item in self.current_order["items"])

    def update_from_json(self, order_data: Dict) -> bool:
        """
        Update the current order with data received from the chatbot's JSON output.
        Returns True if successful, False otherwise.
        """
        try:
            # Update core fields if present
            if "order_id" in order_data:
                self.current_order["order_id"] = order_data["order_id"]
            
            if "status" in order_data:
                # Map chatbot status to system status if needed
                self.current_order["status"] = order_data.get("order_status", "pending")
                
            # Update items if present
            if "items" in order_data:
                self.current_order["items"] = []
                for item in order_data["items"]:
                    self.current_order["items"].append({
                        "name": item.get("item_name", "Unknown Item"),
                        "price": item.get("price_per_item", 0),
                        "quantity": item.get("quantity", 1),
                        "customizations": {"size": item.get("size")} if item.get("size") else {},
                        "item_total": item.get("subtotal", 0)
                    })
            
            # Update totals directly from JSON to ensure consistency with what user agreed to
            self.current_order["total"] = order_data.get("total_amount", 0)
            self.current_order["delivery_fee"] = order_data.get("delivery_fee", 150)
            
            # Infer subtotal and tax if not provided, assuming tax is included or 0
            # If chatbot didn't mention tax, we assume 0 to match total
            self.current_order["tax"] = 0 
            self.current_order["subtotal"] = self.current_order["total"] - self.current_order["delivery_fee"]
            
            return True
        except Exception as e:
            print(f"Error updating order from JSON: {e}")
            return False
