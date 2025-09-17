from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

# 加载JSON文件
json_file_path = r"C:\Users\38308\Desktop\cwe_data.json"
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 自定义加载函数，将JSON转换为文档
def load_json_data(item, additional_fields=None):
    metadata = {"ID": item.get("ID"), "Name": item.get("Name")}
    content = f"Description: {item.get('Description', '')}\nExtended Description: {item.get('Extended_Description', '')}\nPotential Mitigations: {item.get('Potential_Mitigations', [])}\nRelated Attack Patterns: {item.get('Related_Attack_Patterns', [])}"
    return {"page_content": content, "metadata": metadata}

# 使用JSONLoader加载数据
loader = JSONLoader(file_path=json_file_path, jq_schema='.[]', text_content=False, metadata_func=load_json_data)
documents = loader.load()

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 每个chunk约500字符
    chunk_overlap=50,  # 相邻chunk重叠50字符以保持上下文
    length_function=len,
)
chunks = text_splitter.split_documents(documents)

