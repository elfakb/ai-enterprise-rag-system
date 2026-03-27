from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate

def get_response(user_query):
    # HF Embedding Modelini Yükle ve Veritabanındaki metin parçalarını sayısal vektörlere dönüştürür.
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # pdf den aldığımız metin parçalarını içeren vektör veritabanını yükleyoruz. Bu veritabanı, kullanıcının sorusunu döküman parçalarıyla eşleştirmek için kullanılacak.
    vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)
    
    # model llma 3.1 temperature=0.1: Yanıtın deterministik olması için düşük değer. (0 → daha sabit, 1 → daha yaratıcı
    # not : eğer docker da kullanıcaksan ilk oalrak img oluşturmayı unutma sonra da bu OllamaLLM in sonuna base_ur i de ekle 

    llm = OllamaLLM(model="llama3.1", temperature=0.1) # , base_url="http://host.docker.internal:11434"
    
    # prompt şablonu - context : vector db den gelen ayırdığımız veri parçalaro i question : kullanıcı sorusu
    # Model, verilen bağlama sadık kalarak cevap üretir.

    template = """Aşağıdaki bağlamı (context) kullanarak teknik soruyu cevapla. 
    Cevabını dökümana sadık kalarak ver. Bilginin hangi kaynaktan geldiğini belirtmeye çalışma, 
    ben onu sistemden otomatik ekleyeceğim.

    Bağlam: {context}
    Soru: {question}
    Cevap:"""

    # promt şablonu yukardaki template i kullanarak oluşturulur modelin nasıl cevap vermesi gerektiğini tanımlar.
    prompt = ChatPromptTemplate.from_template(template)

   
    # return_source_documents=True diyerek döküman objelerini de istiyoruz
    #
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # "stuff" → tüm bağlamı tek seferde modele verir. Küçük bağlamlar için uygundur.
        retriever=vector_db.as_retriever(search_kwargs={"k": 10}), # 10 her ilgili parçayı getirir
        return_source_documents=True, 
        chain_type_kwargs={"prompt": prompt} # oluşturduğumuz prompt şablonunu kullanarak cevap üretir.
    )

    #
    result = qa_chain.invoke({"query": user_query})
    
    answer = result["result"]
    source_docs = result["source_documents"]
    
    # kaynak gösterme için dökğmandan  çok önemli : bilgileri çekiyoruz ve kullanıcıya sunmak için formatlıyoruz. Aynı kaynaktan gelen bilgileri tek bir satırda göstermek için kaynakları benzersiz hale getiriyoruz.
    sources = []
    for doc in source_docs:
        # metadata içinden dosya adı ve sayfa numarasını çekiyoruz
        source_name = doc.metadata.get("source", "Bilinmeyen Kaynak")
        page_num = doc.metadata.get("page", "?")
        source_info = f"{source_name} (Sayfa: {page_num})"
        if source_info not in sources:
            sources.append(source_info)
    
    formatted_sources = "\n".join([f"- {s}" for s in sources])
    
    # kullanıcıya hem cevap hem de cevaın kaynaklaını göstermek için final bir string oluşturuyoruz.
    final_answer = f"{answer}\n\n**Kaynaklar:**\n{formatted_sources}"
    
    return {"result": final_answer}