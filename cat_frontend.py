#pip install openai
#pip install ctransformers
#pip install chainlit
#chainlit run chat_cat.py -w

import chainlit as cl
import websockets
import asyncio
import json

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    async with websockets.connect("ws://host.docker.internal:1865/ws") as websocket:
        await websocket.send(json.dumps({"text": message.content}))
        while True:
            cat_response = json.loads(await websocket.recv())
            #print("Cheshire Cat:", json.dumps(cat_response, indent=4))
            
            if cat_response["type"] == "chat_token":
                await msg.stream_token(cat_response["content"])
            
            elif cat_response["type"] == "chat":
                msg.content = cat_response["content"] + get_sources(cat_response)
                await msg.update()
                break
            
            else:
                break

# Return sources     
def get_sources(cat_response):
    sources = []
    
    try:
        for declarative_item in cat_response["why"]["memory"]["declarative"]:
            sources.append(declarative_item["metadata"]["source"])
    except Exception as e:
        print(e)
    
    sources = sorted(list(set(sources)))
    
    if len(sources) > 0:
        return "\n\nFonti:\n" + "\n".join([f"- {source}" for source in sources])
    else:
        return ""