import config
import tools
import models
import json
from tool_definitions import tool_definitions
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def run_tool(tool_name, tool_input):
    match tool_name:
        case tools.ToolName.SEARCH_WEB.value:
            result = tools.search_web(tool_input["query"])
        case tools.ToolName.CONVERT_TIMEZONE.value:
            result = tools.convert_timezone(
                tool_input["time_str"],
                tool_input["from_tz"],
                tool_input["to_tz"]
            )
        case tools.ToolName.CALCULATE.value:
            result = tools.calculate(tool_input["expression"])
        case _:
            result = models.Error(
                message=f"Unknown tool: {tool_name}",
                tool_name = tool_name
            )
    models.log_tool_call(result)

    if models.is_success(result):
        return result.data
    else:
        return {"Error": result.message}
    
def strip_embeddings(messages):
    clean = []
    for msg in messages:
        clean.append({"role": msg["role"], "content": msg["content"]})
    return clean

def process_message(messages, user_input):
    embedding = config.embedding_model.encode(user_input)
    messages.append(models.user_message(user_input, embedding))
    
    iteration = 0
    
    while True:
        iteration += 1
        
        if iteration > config.MAX_ITERATIONS:
            return "I hit my tool limit for this request. Please try a simpler question.", messages
        
        response = config.client.messages.create(
            model=config.MODEL,
            max_tokens=config.MAX_TOKENS,
            system=config.SYSTEM_PROMPT,
            tools=tool_definitions,
            messages=strip_embeddings(messages)
        )
        
        if response.stop_reason == "tool_use":
            tool_uses = [block for block in response.content if block.type == "tool_use"]
            messages.append(models.assistant_message(response.content))
            
            tool_results = []
            
            for tool_use in tool_uses:
                tool_name = tool_use.name
                tool_input = tool_use.input
                
                print(f"[Using tool: {tool_name} with input: {tool_input}]")
                
                tool_result = run_tool(tool_name, tool_input)
            
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(tool_result)
                })
            
            messages.append(models.tool_result_message(tool_results))
        
        else:
            reply = response.content[0].text
            embedding = config.embedding_model.encode(reply)
            messages.append(models.assistant_message(reply, embedding))
            return reply, messages