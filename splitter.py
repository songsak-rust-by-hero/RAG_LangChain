# splitter.py
# ไฟล์นี้มีหน้าที่ในการแบ่งเอกสารออกเป็นส่วนย่อยๆ (chunks)
import logging # นำเข้าโมดูล logging สำหรับบันทึกเหตุการณ์ต่างๆ
from langchain_text_splitters import RecursiveCharacterTextSplitter # นำเข้าคลาสสำหรับแบ่งข้อความแบบ recursive
from config import CHUNK_SIZE, CHUNK_OVERLAP, ADD_START_INDEX # นำเข้าการตั้งค่าสำหรับการแบ่งข้อความจากไฟล์ config
from typing import List # นำเข้า List สำหรับการระบุประเภทของข้อมูล
from langchain_core.documents import Document # นำเข้า Document สำหรับจัดการเอกสาร

logger = logging.getLogger(__name__) # สร้าง logger สำหรับไฟล์นี้เพื่อบันทึกข้อความ


def split_documents(docs: List[Document]) -> List[Document]:
    """
    แบ่งเอกสารที่ได้รับมาออกเป็นส่วนย่อยๆ ตามขนาดและส่วนทับซ้อนที่กำหนด
    คืนค่าเป็นลิสต์ของอ็อบเจกต์ Document ที่ถูกแบ่งแล้ว
    """
    if not docs:
       logger.warning("ไม่พบเอกสาร") # บันทึกคำเตือนหากไม่มีเอกสารให้แบ่ง
       return [] # คืนค่าลิสต์ว่างเปล่าหากไม่มีเอกสาร
    text_splitter = RecursiveCharacterTextSplitter( # สร้างอ็อบเจกต์สำหรับแบ่งข้อความ
        chunk_size=CHUNK_SIZE, # ขนาดอักษรต่อ chunk
        chunk_overlap=CHUNK_OVERLAP, # ระยะทับซ้อนเพื่อกันเนื้อหาขาดตอน
        add_start_index=ADD_START_INDEX, # เก็บตำแหน่งเริ่มต้นใน text ต้นฉบับ
        separators=["\n\n","\n"," ",""], # ตัดข้อความในเอกสาร
            )
    all_splits = text_splitter.split_documents(docs) # ทำการแบ่งเอกสารออกเป็นส่วนย่อยๆ
    logger.info(f"Split into {len(all_splits)} sub-documents.") # บันทึกข้อมูลจำนวนเอกสารย่อยที่ได้
    return all_splits # คืนค่าลิสต์ของเอกสารย่อยทั้งหมด