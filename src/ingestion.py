from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter # metni küçük parçalara bölmek için
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# fonksiyonun amacı pdf yi yükle - parçala RescructiveCharacterTextSplitter ile - embedding oluştur free hugging face İLE  - vektör veritabanına kaydet
def process_document(file_path):
    #PDF yükleme ve parçalama RescructiveCharacterTextSplitter ile
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # 2. Parçalara Böl (Llama'nın rahat okuması için)
    #çalışcan text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) chunk_size=1000, chunk_overlap=200 yaparak daha büyük parçalar oluşturuyoruz. Ayrıca soru işaretini de bölme noktası olarak ekledik.
   

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,    # Daha büyük parçalar oluşturuyoruz
        chunk_overlap=200,  # 50 Parçalar arasında biraz örtüşme bırakıyoruz
        separators=["\n\n", "\n", "?", "."] # soruları ve cümle sonlarını bölme noktası olarak aldık
    )
    splits = text_splitter.split_documents(documents) # oluşturulan obeler listesi

    # hugging face embedding ile Her metin parçasını sayısal vektöre dönüştürür.
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4. Vektör DB'ye Kaydet

    vector_db = Chroma(
        persist_directory="./db", 
        embedding_function=embeddings
    )
    vector_db.add_documents(splits) # Yeni döküman eklenir var olanların üzeirne 
    return "Döküman başarıyla veritabanına eklendi!"