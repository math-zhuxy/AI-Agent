import json
import tools
import requests
import set
import tools.file
import tools.search

function_tools = [
    {
        "type": "function",
        "function": {
            "name": "bing search",
            "description": "使用Bing根据关键词进行网络搜索",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索的关键字，必须简洁明了"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web search",
            "description": "根据网站链接直接访问网站",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要搜索网站的链接"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write data",
            "description": "将内容写入到文件中",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "要写入文件名及后缀，比如'main.md'"
                    },
                    "mode_type": {
                        "type": "string",
                        "description": "写入文件的模式，'w'表示覆盖，如果没有则创建；'a'表示追加",
                        "enum": ["w", "a"]
                    },
                    "content": {
                        "type": "string",
                        "description": "写入文件的内容"
                    }
                },
                "required": ["file_path", "mode_type", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read data",
            "description": "读取文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "要读取的文件名及后缀，比如'main.md'"
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]

def model_func_call(user_message: str)-> str:
    all_messages = [
        {
            "role": "system",
            "content": """
                    你是一个能够根据用户指令准确调用相应函数的助手。
                    你的主要任务是从用户的输入中提取出核心指令（输入中包含冗余或无关信息），并选择正确的函数和参数进行调用。
                    """
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
    req_header = {
        "Content-Type": "application/json",
        'Authorization': f'Bearer {set.func_call_api_key}'
    }
    req_data = {
        "model": set.func_call_llm_name,
        "messages": all_messages,
        "tools": function_tools
    }
    model_response = requests.post(url= set.func_call_llm_url, headers=req_header, data=json.dumps(req_data))

    if model_response.status_code != 200:
        print(f"error: can not obtain call func llm info. response code is: {model_response.status_code}")
        return "error"
    
    print("Successfully obtained call func llm info")

    model_response_data = model_response.json()

    if "tool_calls" not in model_response_data["choices"][0]["message"]:
        print("no function called")
        return "null"
    model_tool_call = model_response_data["choices"][0]["message"]["tool_calls"][0]

    llm_called_func_name = model_tool_call["function"]["name"]
    func_args = json.loads(model_tool_call["function"]["arguments"])

    print(f"model try to call {llm_called_func_name} function")
    if llm_called_func_name == "bing search":
        print(f"start calling bing search function, key word is: {func_args['query']}")
        func_result = tools.search.get_bing_search_result(func_args["query"])
        return str(func_result)
    elif llm_called_func_name == "web search":
        print(f"start calling web search function, key word is: {func_args['url']}")
        func_result = tools.search.get_web_search_result(func_args["url"])
        return func_result
    elif llm_called_func_name == "write data":
        print(f"start write content to file: {func_args["file_path"]}")
        func_result = tools.file.write_data(func_args["file_path"], func_args["content"], func_args["mode_type"])
        return func_result
    elif llm_called_func_name == "read data":
        print(f"start read content tin file: {func_args["file_path"]}")
        func_result = tools.file.read_data(func_args["file_path"])
        return func_result
    else:
        print("unknown function type")
        return "error"
