import os
os.environ['OPENAI_API_BASE']='http://localhost:8000/v1'
os.environ['LOCAL_MODEL_NAME']='/root/qwen-7b-chat/'
os.environ['OPENAI_API_KEY']='sk-some_random_chars'
# unset http and https proxy 
os.environ['http_proxy']=''
os.environ['https_proxy']=''
os.environ['SERPAPI_API_KEY']='72615ce2801f5c02b128965fa790dd068445fe2b3dc7eaa4d1e4e15cbc80d554'
os.environ['PINECONE_API_KEY']='b4b4d5e5-1d92-4b3c-8631-baef9b0f5766' 