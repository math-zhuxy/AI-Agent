def write_data(file_path: str, content: str, mode_type: str) -> str:
    try:
        if mode_type != 'w' and mode_type != 'a':
            return "error"
        with open(file_path, mode_type, encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error: {e}")
        return "error"
    return "done"

def read_data(file_path: str) -> str:
    content = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error: {e}")
        return "error"
    return content