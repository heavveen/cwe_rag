from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import json

# 加载JSON文件
json_file_path = r"C:\Users\38308\Desktop\cwe_data.json"
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 自定义文档列表
documents = []
for item in data:
    metadata = {"ID": item.get("ID"), "Name": item.get("Name")}
    content = f"Description: {item.get('Description', '')}\nExtended Description: {item.get('Extended_Description', '')}\nPotential Mitigations: {item.get('Potential_Mitigations', [])}\nRelated Attack Patterns: {item.get('Related_Attack_Patterns', [])}"
    documents.append(Document(page_content=content, metadata=metadata))

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 每个chunk约500字符
    chunk_overlap=50,  # 相邻chunk重叠50字符以保持上下文
    length_function=len,
)
chunks = text_splitter.split_documents(documents)

# 初始化嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 创建FAISS向量存储
vectorstore = FAISS.from_documents(chunks, embeddings)

# 保存向量数据库到本地
vectorstore.save_local("faiss_index")
