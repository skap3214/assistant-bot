# assistant-bot
Goal: The goal is to have an AI assistant that can do anything and everything for you. It has access to as many tools as it needs and will perform any tasks the user gives it. It has access to long term memory, your files, the terminal and much more so that it can perform tasks at just a request by the user.
I currently use Langchain as my foundation to build my bot.

## Features in Progress
Creating an agent that can improve over time. The agent comprises of 3 sub agents:
- Feedback Agent: provides and updates feedback based on the current user interaction
- Planner Agent: creates a step by step plan based on feedback, chat history, tools list
- Executor Agent: Executes the instructions outlined by the Planner agent.

This creates an agent that can improve over time as the user interacts with it more. It sort of reflects on every interaction it has with the user. I have currently added code for this agent in the agent folder.

The feedback plan execute agent code is almost done and you can run it in the combined.py file inside the agent folder. Feedback update has not yet been added but will soon be added once supabase is fully linked to the agent. Once this agent is complete, I will remove the original CustomAgent() class. 

## Current tools it has access to:
- Search (DuckDuckGo)
- SceneXplain (image to text)
- Math
- Python repl
- Gradio Tools (TextToImage, TextToVideo, ImageCaptioning, PromptGenerator)
- ArXiv Tool
- Terminal tool (Opens terminal at current working dir)
- Add Song tool - can add a song to a specific spotify playlist
- Add file link to google drive folder - can add any public file link to google drive (Using IFTTT)
- PlayWright Browser Toolkit

Removed:
requests, file management toolkit

Looking to add much much more.

To run the project you need to create a .env file at root dir with these keys:
```
#AI/LANGCHAIN
OPENAI = 
IFTTT = 
ELEVEN_LABS = 
<!-- PINECONE =  -->
<!-- SERPER =  -->
<!-- GOOGLE =  -->
<!-- APIFY =  -->
#DB
SUPABASE_URL = 
SUPABASE_KEY = 
SCENEXPLAIN = 
```
To run the add song tool, add to google drive tool create an IFTTT applet with a webhook.
Instructions to add an IFTTT webhook over here:
https://python.langchain.com/en/latest/modules/agents/tools/examples/ifttt.html

frontend development in progress (Thinking of using either React native, SwiftUI or Discord)

Navigate to main.py in the root dir and run that file on your terminal after your setup is done OR to try out the new experimental reinforced agent, go to agents/combined and run the test code.

## Persistent Memory
Supbase is used to store the long term memory. By defualt in the initiate_agent() method, the long_term_memory param is 'True'. This will get the memory from the Supabase DB.

To initialise your Supabase DB:
Create a table called history(the name cannot be different)
fields:
id (primary key, int8, auto increment)
created_at (timestampz)
message (varchar)
response (varchar)
verbose (varchar)

The incognito mode, which is a param in the initiate_agent() method as 'incoginto' is Default set to False. If you switch it on. The agent will not save the **new interactions** in the session.

## Transient Memory
Memory currently uses the Langchain implemented ConversationTokenBufferMemory which holds most recent memory maxed to the token limit set. I am in the process of experimenting with combined memory stores but that may take a while.
