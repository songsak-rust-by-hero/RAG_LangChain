# main.py
# ไฟล์นี้เป็นจุดเริ่มต้นของโปรแกรม ทำหน้าที่จัดการขั้นตอนหลักทั้งหมด
import logging # นำเข้าโมดูล logging สำหรับบันทึกเหตุการณ์ต่างๆ
from loader import load_document # นำเข้าฟังก์ชันโหลดเอกสาร
from splitter import split_documents # นำเข้าฟังก์ชันแบ่งเอกสาร
from vectorstore import create_vector_store, search_similar,save_vector_store,load_vector_store # นำเข้าฟังก์ชันจัดการ Vector Store
from llm_handler import get_llm, ask_question # นำเข้าฟังก์ชันจัดการ Large Language Model (LLM)
from config import DEFAULT_K # นำเข้าค่าเริ่มต้น K จากไฟล์ config

# กำหนดค่าเริ่มต้นสำหรับการบันทึก log
logging.basicConfig(
    level=logging.INFO, # กำหนดระดับการบันทึกเป็น INFO
    format="%(asctime)s - %(levelname)s - %(message)s" # กำหนดรูปแบบการแสดงผลของ log
)

# ปิดการแสดงผล log ที่ไม่จำเป็นจากไลบรารีบางตัว เพื่อให้คอนโซลสะอาดขึ้น
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("httpcore").setLevel(logging.ERROR)

def main():
    # ขั้นตอนที่ 1: โหลดเอกสาร
    docs = load_document()
    if not docs:
        logging.error("No documents loaded. Exiting.") # บันทึกข้อผิดพลาดและออกจากโปรแกรมหากโหลดเอกสารไม่สำเร็จ
        return
    
    # ขั้นตอนที่ 2: แบ่งเอกสารออกเป็นส่วนย่อยๆ (chunks)
    all_splits = split_documents(docs)
    if not all_splits: 
        logging.error("No splits created. Exiting.") # บันทึกข้อผิดพลาดและออกจากโปรแกรมหากแบ่งเอกสารไม่สำเร็จ
        return
    
    # ขั้นตอนที่ 3: จัดการ Vector Store (โหลดหรือสร้างใหม่)
    vector_store = load_vector_store() # พยายามโหลด Vector Store ที่มีอยู่แล้ว

    if vector_store is None: # ถ้ายังไม่มี Vector Store
       vector_store = create_vector_store(all_splits) # สร้าง Vector Store ใหม่จากส่วนย่อยของเอกสาร
       if vector_store is None:
          logging.error("Failed to create vector store") # บันทึกข้อผิดพลาดหากสร้าง Vector Store ไม่สำเร็จ
          return

       save_vector_store(vector_store) # บันทึก Vector Store ที่สร้างใหม่ลงดิสก์
       logging.info("Created and saved new vector store") # บันทึกข้อมูลว่าสร้างและบันทึก Vector Store ใหม่แล้ว
    else:
           logging.info("Loaded existing vector store") # บันทึกข้อมูลว่าโหลด Vector Store ที่มีอยู่แล้ว
    
    # ขั้นตอนที่ 4: ทดสอบการค้นหาเอกสารที่คล้ายกัน
    print("\n--- Test search: 'What is an Deep Agents overview?' ---")
    results = search_similar(vector_store, "What is an Deep Agents overview", k=DEFAULT_K) # ค้นหาเอกสารที่คล้ายกับคำถาม
    for doc in results:
        print(doc.page_content[:500]) # แสดงเนื้อหา 500 ตัวอักษรแรกของแต่ละผลลัพธ์
        print("------")
    
    # ขั้นตอนที่ 5: ถามคำถามโดยใช้ LLM และบริบทจาก Vector Store
    print("\n--- Question: 'Deep Agents overview คืออะไร' ---")
    llm = get_llm() # สร้างอ็อบเจกต์ LLM
    question = "Deep Agents overview คืออะไร" # กำหนดคำถาม
    docs_for_answer = search_similar(vector_store, question, k=DEFAULT_K) # ค้นหาเอกสารที่เกี่ยวข้องกับคำถาม
    context = "\n\n".join(d.page_content for d in docs_for_answer) # รวมเนื้อหาจากเอกสารที่เกี่ยวข้องเพื่อใช้เป็นบริบท
    answer = ask_question(llm, context, question) # ถามคำถามกับ LLM โดยใช้บริบทที่ได้มา
    print(f"Answer: {answer}") # แสดงคำตอบที่ได้จาก LLM

if __name__ == "__main__":
    main() # เรียกใช้ฟังก์ชัน main เมื่อสคริปต์ถูกรันโดยตรง