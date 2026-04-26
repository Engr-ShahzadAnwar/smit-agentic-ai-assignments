import os
import google.generativeai as genai
from dotenv import load_dotenv
from weather_api import get_weather, format_weather_response

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the weather tool for function calling
weather_tool = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="get_weather",
            description="Get the current weather for a specific city. Use this when users ask about weather conditions, temperature, or climate in a particular location.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "city": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="The name of the city to get weather for (e.g., 'London', 'New York', 'Tokyo')"
                    )
                },
                required=["city"]
            )
        )
    ]
)

# Initialize the model with function calling
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    tools=[weather_tool]
)


class ChatbotEngine:
    """Chatbot engine with weather function calling capabilities."""
    
    def __init__(self):
        self.chat = model.start_chat(enable_automatic_function_calling=False)
    
    def process_message(self, user_message: str) -> tuple[str, bool]:
        """
        Process user message and return response.
        
        Args:
            user_message: The user's input message
            
        Returns:
            Tuple of (response_text, function_called)
        """
        try:
            # Send message to Gemini
            response = self.chat.send_message(user_message)
            
            # Check if function calling is requested
            function_called = False
            
            # Handle function calls
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if fn_call := part.function_call:
                        function_called = True
                        
                        # Execute the function call
                        if fn_call.name == "get_weather":
                            city = fn_call.args["city"]
                            
                            # Call the actual weather API
                            weather_data = get_weather(city)
                            
                            # Send the function result back to the model
                            function_response = genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name="get_weather",
                                    response={"result": weather_data}
                                )
                            )
                            
                            # Get the final response from the model
                            final_response = self.chat.send_message(function_response)
                            return final_response.text, function_called
            
            # No function call, return regular response
            return response.text, function_called
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}", False
    
    def reset_chat(self):
        """Reset the chat history."""
        self.chat = model.start_chat(enable_automatic_function_calling=False)
