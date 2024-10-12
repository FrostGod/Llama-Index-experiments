from llama_index.core.tools import FunctionTool
import os

def code_read_func(file_path: str):
  path = os.path.join("data", file_path)
  try:
    with open(path, "r") as file:
      content = file.read()
      return {"file_content": content}
  except Exception as e:
    return {"error": e}
  
code_reader = FunctionTool(
  fn=code_read_func,
  name="code_reader",
  description="This tool reads the contents of the code file, and returns the result. use this tool when you need to read the contents of a file."
)