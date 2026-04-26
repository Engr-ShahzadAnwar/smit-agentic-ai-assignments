from agent import CryptoAgent

def main():
    agent = CryptoAgent()
    print("Crypto Knowledge-First Agent Initialized.")
    print("Ask about coins (e.g., 'Tell me about Bitcoin', 'What is its price?').")
    print("Type 'exit' to quit.")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            response = agent.process_query(user_input)
            
            # The agent returns a dict, but we want the formatted string if available
            if "formatted" in response:
                print(response["formatted"])
            else:
                 # It was a rejection
                 print(response["answer"]) # Should be the rejection message

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
