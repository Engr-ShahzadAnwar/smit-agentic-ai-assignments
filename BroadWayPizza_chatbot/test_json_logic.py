from order_manager import OrderManager

def test_json_update():
    om = OrderManager()
    
    # Mock JSON data from chatbot
    mock_data = {
        "order_id": "BP9999",
        "order_status": "confirmed",
        "items": [
            {
                "item_name": "Dancing Fajita",
                "price_per_item": 1299,
                "quantity": 2,
                "size": "Large",
                "subtotal": 2598
            }
        ],
        "delivery_fee": 150,
        "total_amount": 2748
    }
    
    print("Initial Order:", om.get_current_order())
    
    success = om.update_from_json(mock_data)
    
    if success:
        print("\nUpdate Successful!")
        print("Updated Order:", om.get_current_order())
        
        # Verify specific fields
        order = om.get_current_order()
        assert order["order_id"] == "BP9999"
        assert len(order["items"]) == 1
        assert order["items"][0]["name"] == "Dancing Fajita"
        assert order["items"][0]["quantity"] == 2
        assert order["total"] == 2748
        print("\nAll assertions passed!")
    else:
        print("\nUpdate Failed.")

if __name__ == "__main__":
    test_json_update()
