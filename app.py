import streamlit as st
import os
import shutil
from src.ingestion import process_document
from src.chat import get_response

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Llama 3 Enterprise RAG", layout="wide")


with st.sidebar:
    st.header("Sistem Yönetimi -BELGE EKLEME & SIFIRLAMA-")
    
    # SIFIRLAMA BUTONU - Her şeyden önce ve en üstte
    if st.button("Veritabanını Sıfırla", use_container_width=True):
        try:
            # Vektör veritabanını temizle
            if os.path.exists("./db"):
                shutil.rmtree("./db")
            # Yüklenen PDF'leri temizle data klasöründen
            if os.path.exists("data"):
                for file in os.listdir("data"):
                    file_path = os.path.join("data", file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            
            st.success("Sistem başarıyla sıfırlandı!")
            st.rerun() 
        except Exception as e:
            st.error(f"Sıfırlama hatası: {e}")

    st.divider() 

    st.header("📁 Veri Girişi")
    uploaded_file = st.file_uploader("Bir PDF dökümanı yükle", type="pdf")
    
    if st.button("Veritabanına İşle", use_container_width=True):
        if uploaded_file:
            # Data klasörü yoksa oluştur
            if not os.path.exists("data"):
                os.makedirs("data")
                
            file_path = f"data/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Döküman analiz ediliyor..."):
                try:
                    msg = process_document(file_path)
                    st.success(msg)
                except Exception as e:
                    st.error(f"İşleme Hatası: {e}")
        else:
            st.warning("Lütfen önce bir dosya seçin!")

# Ana Ekran 
st.title("🦙 Llama 3 Kurumsal RAG Sistemi")
st.info("Bu sistem yerel Llama 3.1 modelini kullanarak dökümanlarınız üzerinden analiz yapar.")

# Sohbet Alanı
query = st.text_input("Dökümanlarınla ilgili bir soru sor:")

if query:
    with st.spinner("Llama 3 dökümanları tarıyor..."):
        try:
            response = get_response(query)
            
            st.markdown("### Cevap:")
            st.write(response["result"]) # bunu son haline göre aldık
            
            # Kaynakları gösterme 
            if "source_documents" in response:
                with st.expander("📚 Kullanılan Kaynaklar"):
                    for doc in response["source_documents"]:
                        source = doc.metadata.get("source", "Bilinmiyor")
                        page = doc.metadata.get("page", "-")
                        st.write(f"- **Dosya:** {source} (Sayfa: {page})")
        except Exception as e:
            st.error(f"Sorgu Hatası: {e}")