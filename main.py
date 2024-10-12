from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from prompts import context
from code_reader import code_reader
from dotenv import load_dotenv

load_dotenv()
llm = Ollama(model="llama3.2:1b", request_timeout=30.0)

# result = llm.complete("What is the capital of France?")

# print(result)

parser = LlamaParse(result_type="markdown")

fileExtractor = {".pdf": parser}

documents = SimpleDirectoryReader("./data", file_extractor=fileExtractor).load_data()
embed_model = resolve_embed_model("local:BAAI/bge-m3")
vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
query_engine = vector_index.as_query_engine(llm=llm)

# result = query_engine.query("What is the transfer amount?")
# print(result)

tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
          name="bank_statement_query",
          description="Use this tool to answer questions about the bank statement"
        )
    ),
    code_reader
]

code_llm = Ollama(model="codellama", request_timeout=60.0)
agent = ReActAgent.from_tools(tools, llm=code_llm, verbose=True, context=context)

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    print("Prompt: ", prompt)
    result = agent.query(prompt)
    print(result)