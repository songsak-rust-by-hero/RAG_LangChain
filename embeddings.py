# embeddings.py
# ไฟล์นี้มีหน้าที่จัดการและสร้าง Embedding Model สำหรับการแปลงข้อความเป็นเวกเตอร์
from langchain_huggingface import HuggingFaceEmbeddings # นำเข้าคลาสสำหรับสร้าง Embeddings จาก Hugging Face
from config import EMBEDDING_MODEL # นำเข้าชื่อโมเดล Embedding ที่กำหนดไว้ในไฟล์ config

def get_embeddings():
    """
    สร้างและคืนค่าอ็อบเจกต์ HuggingFaceEmbeddings ที่ตั้งค่าด้วยชื่อโมเดลที่กำหนด
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL # กำหนดชื่อโมเดล Embedding ที่จะใช้
    )
    return embeddings # คืนค่าอ็อบเจกต์ Embeddings