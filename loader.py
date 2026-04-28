# loader.py
# ไฟล์นี้มีหน้าที่ในการโหลดเอกสารจากแหล่งข้อมูลเว็บ
from langchain_community.document_loaders import PlaywrightURLLoader # นำเข้า WebBaseLoader สำหรับโหลดเอกสารจาก URL
import logging # นำเข้าโมดูล logging สำหรับบันทึกเหตุการณ์ต่างๆ
from typing import List # นำเข้า List สำหรับการระบุประเภทของข้อมูล
from langchain_core.documents import Document # นำเข้า Document สำหรับจัดการเอกสาร
from config import WEB_PATH

logger = logging.getLogger(__name__) # สร้าง logger สำหรับไฟล์นี้เพื่อบันทึกข้อความ

def load_document() -> List[Document]:
    """
    โหลดเอกสารจาก URL ที่กำหนดโดยใช้ WebBaseLoader และตัวกรอง BeautifulSoup
    คืนค่าเป็นลิสต์ของอ็อบเจกต์ Document
    """
    loader = PlaywrightURLLoader([WEB_PATH])
    docs = loader.load() # เริ่มต้นการโหลดเอกสารจากหน้าเว็บ
    if not docs:
        logger.warning("No documents loaded") # บันทึกคำเตือนหากไม่มีเอกสารถูกโหลด
        return [] # คืนค่าเป็นลิสต์ว่างเปล่า
    logger.info(f"Total characters: {len(docs[0].page_content)}") # บันทึกจำนวนอักขระทั้งหมดในเอกสารที่โหลดมา
    return docs # คืนค่าลิสต์ของเอกสารที่โหลดมา