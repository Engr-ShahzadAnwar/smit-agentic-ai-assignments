# AI Agentic Class Assignments

## Overview
This repository contains a collection of Artificial Intelligence projects and chatbots developed as part of the **SMIT Batch 8 AI Agentic** course. These projects demonstrate the practical application of Large Language Models (LLMs), Generative AI, and Agentic workflows to solve real-world problems.

The primary focus of these assignments is to build intelligent agents capable of reasoning, function calling, and maintaining context-aware conversations using modern AI frameworks.

## Directory Structure
The repository is organized into distinct project folders, each containing a standalone application:

- **BroadWayPizza_chatbot/**  
  A specialized restaurant chatbot designed to handle customer orders, answer menu queries, and manage reliance interactions. It involves structured data handling and intent recognition.

- **Crypto Agent/**  
  An intelligent financial agent that tracks cryptocurrency prices, builds market dashboards, and provides market insights. It likely mimics platforms like Binance for data visualization and analysis.

- **weather_chatbot/**  
  A real-time functional agent capable of fetching and interpreting weather data for specific locations. This project demonstrates the usage of external APIs and tool calling within an agentic loop.

## Projects Descriptions

### 1. BroadWay Pizza Chatbot
- **Domain**: Food & Beverage / Customer Service
- **Key Features**: Interactive ordered menu, cart management, system prompting for waitstaff persona.
- **Goal**: To simulate a conversational ordering experience similar to real-world food delivery apps.

### 2. Crypto Analysis Agent
- **Domain**: Finance / Data Analysis
- **Key Features**: Live price tracking, market trend analysis, UI for financial data visualization.
- **Goal**: To apply AI in interpreting complex numerical data and providing actionable insights for traders.

### 3. Weather Assistant
- **Domain**: Utilities / Information Retrieval
- **Key Features**: Location-based weather lookups, natural language interpretation of meteorological data.
- **Goal**: To master function calling and API integration (e.g., OpenWeatherMap) within an LLM workflow.

## Technologies Used
The projects within this repository utilize a modern AI and web development stack:

- **Language**: Python 3.10+
- **Frontend Framework**: Streamlit (for building interactive web UIs)
- **AI Models**: Google Gemini API (Generative AI)
- **Orchestration**: LangChain / Custom Agent Loops
- **Data Handling**: JSON, Pandas
- **Environment Management**: Python-dotenv

## Learning Objectives
Through these assignments, the following core competencies were developed:
- **Prompt Engineering**: Crafting robust system prompts to define agent personas and guardrails.
- **Agentic Workflows**: Implementing loop-based reasoning (Observation -> Thought -> Action).
- **Function Calling**: Enabling LLMs to interact with external tools and APIs.
- **State Management**: Handling session state in Streamlit to maintain conversation history.
- **UI/UX Design**: Creating professional, user-friendly interfaces for AI applications.

## How to Run the Projects
Each project is designed to run independently. Follow these general steps to execute any of the included applications:

1.  **Prerequisites**: Ensure Python and Pip are installed on your system.
2.  **Navigate to the Project Folder**:
    ```bash
    cd <project_folder_name>
    # Example: cd weather_chatbot
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables**:
    - Create a `.env` file in the project root.
    - Add your API keys (e.g., `GEMINI_API_KEY=your_key_here`).
5.  **Run the Application**:
    ```bash
    streamlit run app.py
    # Note: Main entry file might vary (e.g., main.py or chatbot.py)
    ```

## Notes for Reviewers
- These projects are educational assignments and may serve as prototypes rather than production-ready software.
- Valid API keys (specifically Google Gemini) are required for the AI functionalities to work.
- The Git configuration tracks the entire assignment collection.

## Future Improvements
- **Integration**: Combining individual agents into a "Multi-Agent System" (MAS).
- **Persistence**: Adding database support (SQLite/PostgreSQL) for saving user history.
- **Deployment**: containerizing applications using Docker for easier distribution.

## Author
**Student, SMIT Batch 8 - AI Agentic**  
*Exploring the frontiers of Generative AI and Agentic Systems.*
