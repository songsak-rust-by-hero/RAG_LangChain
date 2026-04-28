# vectorstore.py
# ไฟล์นี้มีหน้าที่จัดการ Vector Store สำหรับการจัดเก็บและค้นหาเอกสารแบบเวกเตอร์
from langchain_community.vectorstores import FAISS # นำเข้า FAISS ซึ่งเป็น Vector Store แบบ In-memory
from embeddings import get_embeddings # นำเข้าฟังก์ชันสำหรับสร้าง Embedding จากไฟล์ embeddings.py
from langchain_core.documents import Document # นำเข้า Document สำหรับจัดการเอกสาร
from typing import List # นำเข้า List สำหรับการระบุประเภทของข้อมูล
import os # นำเข้าโมดูล os สำหรับจัดการกับระบบไฟล์
import logging # นำเข้าโมดูล logging สำหรับบันทึกเหตุการณ์ต่างๆ

logger = logging.getLogger(__name__) # สร้าง logger สำหรับไฟล์นี้เพื่อบันทึกข้อความ

def create_vector_store(documents: List[Document]):
    """
    สร้าง Vector Store ด้วย FAISS จากลิสต์ของเอกสารที่ให้มา
    """
    if not documents:
       # หากไม่มีเอกสารเข้ามา จะไม่สร้าง Vector Store
       return None
    
    embeddings = get_embeddings() # สร้างอ็อบเจกต์ Embedding Model
    vector_store = FAISS.from_documents( # สร้าง FAISS Vector Store จากเอกสาร
        documents, # เอกสารที่จะนำไปสร้างเวกเตอร์
        embeddings # โมเดลสำหรับสร้างเวกเตอร์
    )
    return vector_store # คืนค่า Vector Store ที่สร้างขึ้นมา

def save_vector_store(vector_store, path="faiss_index"):
    """
    บันทึก Vector Store ลงในดิสก์ที่พาธที่กำหนด
    """
    if vector_store is None:
        logger.warning("No vector store to save") # บันทึกคำเตือนหากไม่มี Vector Store ให้บันทึก
        return
    vector_store.save_local(path) # บันทึก Vector Store ลงในโฟลเดอร์ที่ระบุ
    logger.info(f"Vector store saved to {path}") # บันทึกข้อมูลว่า Vector Store ถูกบันทึกแล้ว

    if os.path.exists(path):
        logger.info(f"Confirmed: {path} directory created") # ยืนยันว่าโฟลเดอร์ถูกสร้างสำเร็จ
    else:
        logger.error(f"Failed to create {path} directory") # บันทึกข้อผิดพลาดหากสร้างโฟลเดอร์ไม่ได้

def search_similar(vector_store, query: str, k: int = 4):
    """
    ค้นหาเอกสารที่คล้ายกันใน Vector Store ตามคำค้น (query)
    """
    if vector_store is None:
       # หากไม่มี Vector Store จะไม่ทำการค้นหา
       return []
    
    if not query.strip():
       # หากคำค้นว่างเปล่า จะไม่ทำการค้นหา
       return []
    results = vector_store.similarity_search(query, k=k) # ค้นหาเอกสารที่คล้ายกับ query
    return results # คืนค่าผลลัพธ์ของการค้นหา

def load_vector_store(path="faiss_index"):
    """
    โหลด Vector Store ที่บันทึกไว้จากดิสก์
    """
    if not os.path.exists(path):
       # หากไม่พบไฟล์ Vector Store จะไม่สามารถโหลดได้
       return None
    embeddings = get_embeddings() # สร้างอ็อบเจกต์ Embedding Model อีกครั้งเพื่อใช้ในการโหลด
    # โหลด FAISS Vector Store จากพาธที่กำหนด
    # allow_dangerous_deserialization=True จำเป็นสำหรับบางเวอร์ชันหรือเมื่อโหลดจากแหล่งที่ไม่น่าเชื่อถือ
    vector_store = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True) 
    return vector_store # คืนค่า Vector Store ที่โหลดมา