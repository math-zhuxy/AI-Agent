import json
import string
import sys
try:
    with open("setting.json", "r", encoding= "utf-8") as file:
        setting_data = json.load(file)

    chat_llm_url: string = setting_data["model"]["chat"]["url"]
    chat_llm_api_key: string = setting_data["model"]["chat"]["apikey"]
    chat_llm_name: string = setting_data["model"]["chat"]["name"]

    func_call_llm_url: string = setting_data["model"]["func_call"]["url"]
    func_call_api_key: string = setting_data["model"]["func_call"]["apikey"]
    func_call_llm_name: string = setting_data["model"]["func_call"]["name"]

    bing_cookie: string = setting_data["search"]["bing_cookie"]

    print("init program done")
    
except Exception as e:
    sys.exit(f"Error: {e}")