# llm_handler.py
# ไฟล์นี้มีหน้าที่จัดการการเชื่อมต่อและการเรียกใช้ Large Language Model (LLM)
from langchain_groq import ChatGroq # นำเข้าคลาส ChatGroq สำหรับเชื่อมต่อกับโมเดล Groq
from config import GROQ_MODEL, TEMPERATURE # นำเข้าชื่อโมเดลและค่าควบคุมความสุ่มจาก ไฟล์config

def get_llm():
    """
    สร้างและคืนค่าอ็อบเจกต์ LLM ที่ตั้งค่าด้วยโมเดลและอุณหภูมิที่กำหนด
    """
    llm = ChatGroq(
        model=GROQ_MODEL, # กำหนดโมเดลที่จะใช้
        temperature=TEMPERATURE # กำหนดค่าความสุ่มของคำตอบ
    )
    return llm

def ask_question(llm, context, question):
    """
    ส่งคำถามไปยัง LLM พร้อมกับบริบทที่กำหนด และคืนค่าคำตอบที่ได้
    """
    response = llm.invoke(
       f"""
You are a strict QA system.

Rules:
- Answer ONLY using the provided context.
- Do NOT use any external knowledge.
- If the answer is not in the context, say: "Not found in context."
- Do not explain where the answer comes from. 
{context} # บริบทสำหรับตอบคำถาม

Question: # คำถามที่จะถาม
{question}
"""
    )
    return response.content # คืนค่าเฉพาะเนื้อหาของคำตอบจาก LLM