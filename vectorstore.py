# vectorstore.py
# ไฟล์นี้มีหน้าที่จัดการ Vector Store สำหรับการจัดเก็บและค้นหาเอกสารแบบเวกเตอร์
from langchain_community.vectorstores import FAISS # นำเข้า FAISS ซึ่งเป็น Vector Store แบบ In-memory
from embeddings import get_embeddings # นำเข้าฟังก์ชันสำหรับสร้าง Embedding จากไฟล์ embeddings.py
from langchain_core.documents import Document # นำเข้า Document สำหรับจัดการเอกสาร
from typing import List, Optional,Tuple
from langchain_core.vectorstores import VectorStore
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

def save_vector_store(vector_store: Optional[FAISS], path: str="faiss_index")->None:
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

def search_similar(
    vector_store: Optional[VectorStore], # อ็อบเจกต์ Vector Store ซึ่งอาจเป็น None ได้
    query: str, # คำค้นหาที่เป็นสตริง
    k: int = 4 # จำนวนเอกสารที่ต้องการดึงกลับมา ค่าเริ่มต้นคือ 4
) -> List[Document]: # ระบุประเภทของค่าที่ฟังก์ชันจะคืนกลับมา (ลิสต์ของ Document)
    """
    ค้นหาโดยไม่ใส่คะแนน
    """
    # ตรวจสอบว่ามี Vector Store ถูกส่งเข้ามาหรือไม่
    if vector_store is None:
        logger.warning("Vector store is None") # บันทึกคำเตือนหาก vector store เป็น None
        return [] # คืนค่าลิสต์ว่างเปล่า

    # ตรวจสอบความถูกต้องของคำค้นหาและค่า k โดยเรียกใช้ฟังก์ชัน _validate_query
    query = _validate_query(query, k)
    
    try:
        # ทำการค้นหาเอกสารที่คล้ายกันใน Vector Store
        return vector_store.similarity_search(query, k=k)
    except Exception as e:
        # จัดการข้อผิดพลาดที่อาจเกิดขึ้นระหว่างการค้นหา
        logger.error(f"Search error: {e}") # บันทึกข้อผิดพลาดที่เกิดขึ้น
        return [] # คืนค่าลิสต์ว่างเปล่าในกรณีที่เกิดข้อผิดพลาด

def search_similar_with_score(
    vector_store: Optional[VectorStore], # อ็อบเจกต์ Vector Store ซึ่งอาจเป็น None ได้
    query: str, # คำค้นหาที่เป็นสตริง
    k: int = 4 # จำนวนเอกสารที่ต้องการดึงกลับมา ค่าเริ่มต้นคือ 4
) -> List[Tuple[Document, float]]: # ระบุประเภทของค่าที่ฟังก์ชันจะคืนกลับมา (ลิสต์ของ Tuple ที่มี Document และ float)
    """
    ค้นหาและใช้คะแนนด้วย
    """
    # ตรวจสอบว่ามี Vector Store ถูกส่งเข้ามาหรือไม่
    if vector_store is None:
        logger.warning("Vector store is None") # บันทึกคำเตือนหาก vector store เป็น None
        return [] # คืนค่าลิสต์ว่างเปล่า

    # ตรวจสอบความถูกต้องของคำค้นหาและค่า k โดยเรียกใช้ฟังก์ชัน _validate_query
    query = _validate_query(query, k)

    try:
        # ทำการค้นหาเอกสารที่คล้ายกันใน Vector Store พร้อมกับคืนค่าคะแนนความคล้ายคลึง
        return vector_store.similarity_search_with_score(query, k=k)
    except Exception as e:
        # จัดการข้อผิดพลาดที่อาจเกิดขึ้นระหว่างการค้นหา
        logger.error(f"Search error: {e}") # บันทึกข้อผิดพลาดที่เกิดขึ้น
        return [] # คืนค่าลิสต์ว่างเปล่าในกรณีที่เกิดข้อผิดพลาด

def load_vector_store(path: str="faiss_index"):
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

def _validate_query(query: str, k: int): 
    """
    ฟังก์ชันภายในสำหรับตรวจสอบความถูกต้องของคำค้นหาและค่า k
    ลบช่องว่างที่อยู่หน้าและหลังคำค้นหา
    """
    query = query.strip()
    # ตรวจสอบว่าคำค้นหาว่างเปล่าหรือไม่
    if not query:
        raise ValueError("Query is empty") # แจ้งข้อผิดพลาดถ้าคำค้นหาว่างเปล่า
    # ตรวจสอบว่าค่า k เป็นบวกหรือไม่
    if k <= 0:
        raise ValueError("k must be > 0") # แจ้งข้อผิดพลาดถ้า k ไม่มากกว่า 0
    return query # คืนค่าคำค้นหาที่ผ่านการตรวจสอบและทำความสะอาดแล้ว