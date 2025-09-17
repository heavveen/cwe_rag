from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os

# 设置DeepSeek API环境变量
os.environ["OPENAI_API_KEY"] = "sk-5b13e01a35044b8c9ceed1203ff0b4ca"  # 替换为你的DeepSeek API密钥
os.environ["OPENAI_API_BASE"] = "https://api.deepseek.com"

# 初始化嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 加载FAISS向量存储
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# 配置DeepSeek Chat
llm = ChatOpenAI(
    model_name="deepseek-chat",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_API_BASE"],
    temperature=0.7
)

# 创建RAG链
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True
)

# 交互式循环
while True:
    choice = input("Enter 1 to ask a question, 0 to exit: ")
    if choice == "0":
        print("Exiting program...")
        break
    elif choice == "1":
        query = input("Please enter your question: ")
        result = qa_chain.invoke({"query": query})
        print("Question:", query)
        print("Answer:", result["result"])
        print("\nRetrieved Documents:")
        for i, doc in enumerate(result["source_documents"]):
            print(f"Doc {i + 1}:")
            print(doc.page_content[:200] + "...")
            print(f"Metadata: ID={doc.metadata['ID']}, Name={doc.metadata['Name']}")
            print("-" * 50)
    else:
        print("Invalid input! Please enter 0 or 1.")