# assistant-bot
Goal: The goal is to have an AI assistant that can do anything and everything for you. It has access to as many tools as it needs and will perform any tasks the user gives it. It has access to long term memory, your files, the terminal and much more so that it can perform tasks at just a request by the user.
I currently use Langchain as my foundation to build my bot.

## Current tools it has access to:
- Search (DuckDuckGo)
- SceneXplain (image to text)
- Math
- File management(temporarily disabled because it does not work :) )
- Python repl
- Gradio Tools (TextToImage, TextToVideo, ImageCaptioning, PromptGenerator)
- ArXiv Tool
- Terminal tool (Opens terminal at current working dir)
- requests tool - can parse through webpages
- Add Song tool - can add a song to a specific spotify playlist

Looking to add much much more.

To run the project you need to create a .env file at root dir with these keys:
```
#AI/LANGCHAIN
OPENAI = 
<!-- PINECONE =  -->
<!-- SERPER =  -->
<!-- GOOGLE =  -->
<!-- ELEVEN_LABS =  -->
<!-- APIFY =  -->
IFTTT = 
#DB
SUPABASE_URL = 
SUPABASE_KEY = 
SCENEXPLAIN = 
```
To run the add song tool, create an IFTTT applet with a webhook.
Instructions to add a spotify song over here:
https://python.langchain.com/en/latest/modules/agents/tools/examples/ifttt.html

I have not setup UI or any sort of concrete frontend for the application. For now you will have to make do with the terminal.

Navigate to tools/main.py and run that file on your terminal.

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

will add more fields later

The incognito mode, which is a param in the initiate_agent() method as 'incoginto' is Default set to False. If you switch it on. The agent will not save the **new interactions** in the session.

## Transient Memory
Memory currently uses the Langchain implemented ConversationTokenBufferMemory which holds most recent memory maxed to the token limit set. I am in the process of experimenting with combined memory stores but that may take a while.

