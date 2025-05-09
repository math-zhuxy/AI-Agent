import openai
import set
from . import func_model
sys_msg = ""
with open("llm/prompt.md", "r", encoding= "utf-8") as file:
    sys_msg = file.read()
UserMessageList = [
    {
        "role": "system",
        "content": sys_msg
    }
]
ModelStruct = openai.OpenAI(
    api_key = set.chat_llm_api_key, 
    base_url = set.chat_llm_url
)

def communicate_with_llm(user_input: str) -> str:
    UserMessageList.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    while True:
        try:
            model_response = ModelStruct.chat.completions.create(
                model= set.chat_llm_name,
                messages=UserMessageList
            )
        except Exception as e:
            print(f"chat model communicate error: {e}")
            return "Error"
        print("Successfully obtained chat llm info")
        try:
            assistant_message = model_response.choices[0].message
            UserMessageList.append({
                "role": assistant_message.role,
                "content": assistant_message.content
            })
        except Exception as e:
            print(f"analysis chat llm response data error:{e}")
            return "error"
        print(f"LLM instruction: {assistant_message.content}")
        if assistant_message.content.startswith("全部任务已完成"):
            print("finish task.")
            break
        func_result = func_model.model_func_call(assistant_message.content)
        if func_result == "null":
            print("finish task.")
            break
        elif func_result == "error":
            return "Error"
        UserMessageList.append({
            "role": "user",
            "content": func_result
        })
    return "done"