import llm.chat_model
if __name__ == "__main__":
    user_request = input("请输入你想要AI-Agent完成的任务：")
    llm.chat_model.communicate_with_llm(user_request)