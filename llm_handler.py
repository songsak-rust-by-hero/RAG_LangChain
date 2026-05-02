# llm_handler.py
# ไฟล์นี้มีหน้าที่จัดการการเชื่อมต่อและการเรียกใช้ Large Language Model (LLM)
from langchain_groq import ChatGroq # นำเข้าคลาส ChatGroq สำหรับเชื่อมต่อกับโมเดล Groq
from config import GROQ_MODEL, TEMPERATURE # นำเข้าชื่อโมเดลและค่าควบคุมความสุ่มจาก ไฟล์config
from typing import Any

def get_llm():
    """
    สร้างและคืนค่าอ็อบเจกต์ LLM ที่ตั้งค่าด้วยโมเดลและอุณหภูมิที่กำหนด
    """
    llm = ChatGroq(
        model=GROQ_MODEL, # กำหนดโมเดลที่จะใช้
        temperature=TEMPERATURE # กำหนดค่าความสุ่มของคำตอบ
    )
    return llm

def ask_question(llm:Any, context: str, question: str) -> str:
    """
    ส่งคำถามไปยัง LLM พร้อมกับบริบทที่กำหนด และคืนค่าคำตอบที่ได้
    """
    response = llm.invoke(
      f"""
You are a QA system.

Rules:
- Answer using ONLY the provided context.
- If the answer is not in the context, say: "Not found in context."
- Rewrite the answer in your own words.
- Keep the answer concise and clear.
- Do NOT copy text verbatim unless necessary.
- If the context contains steps or a process, include them in the answer. 
{context} # บริบทสำหรับตอบคำถาม

Question: # คำถามที่จะถาม
{question}
"""
    )
    return response.content # คืนค่าเฉพาะเนื้อหาของคำตอบจาก LLM