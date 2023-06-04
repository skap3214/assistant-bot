# assistant-bot
Goal: The goal is to have an AI assistant that can do anything and everything for you. It has access to as many tools as it needs and will perform any tasks the user gives it. It has access to long term memory, your files, the terminal and much more so that it can perform tasks at just a request by the user.
I currently use Langchain as my foundation to build my bot.

## Current tools it has access to:
- Search (DuckDuckGo)
- SceneXplain (image to text)
- Math
- File management(temporarily disabled due to unsupported langchain agent)
- Python repl
- Gradio Tools (TextToImage, TextToVideo, ImageCaptioning, PromptGenerator)
- ArXiv Tool
- Terminal tool (Opens terminal at current working dir)

Looking to add much much more.

To run the project you need to create a .env file at root dir with these keys:
#AI/LANGCHAIN
OPENAI = 
<!-- PINECONE =  -->
<!-- SERPER =  -->
<!-- GOOGLE =  -->
<!-- ELEVEN_LABS =  -->
<!-- APIFY =  -->
#DB
SUPABASE_URL = 
SUPABASE_KEY = 
SCENEXPLAIN = 

## Persistent Memory
Supabase url and incognito mode features will be added later and I currently only have boilerplate code added.

## Transient Memory
Memory currently uses the Langchain implemented ConversationTokenBufferMemory which holds most recent memory maxed to the token limit set. I am in the process of experimenting with combined memory stores but that may take a while.

