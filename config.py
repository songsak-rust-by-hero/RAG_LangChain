# config.py
# ไฟล์นี้เก็บการตั้งค่าและการกำหนดค่าต่างๆ ที่ใช้ทั่วทั้งโปรเจกต์

file_doc= "AI_RAG_TestDocument.docx" #โหลดไฟล์doc

# Text splitter config (การตั้งค่าสำหรับการแบ่งข้อความ)
CHUNK_SIZE = 800 # ขนาดสูงสุดของแต่ละส่วนย่อย (chunk) ของข้อความ
CHUNK_OVERLAP = 100 # จำนวนอักขระที่ทับซ้อนกันระหว่างส่วนย่อย (chunk) เพื่อรักษาบริบท
ADD_START_INDEX = True # ระบุว่าจะเพิ่มดัชนีเริ่มต้นของแต่ละส่วนย่อยใน metadata หรือไม่

# Embedding model (การตั้งค่าสำหรับโมเดล Embedding)
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2" # ชื่อโมเดลที่จะใช้ในการสร้างเวกเตอร์ (embedding) ของข้อความ

# LLM config (การตั้งค่าสำหรับ Large Language Model)
GROQ_MODEL = "llama-3.3-70b-versatile" # ชื่อโมเดล Groq LLM ที่จะใช้งาน
TEMPERATURE = 0 # ค่า Temperature: 
                # < 0.3 = เน้นข้อเท็จจริง/Code (Strict)
                # 0.4 - 0.7 = แชททั่วไป/สรุปความ (Balanced)
                # > 0.8 = งานสร้างสรรค์/ระดมสมอง (Creative)

# Search config (การตั้งค่าสำหรับการค้นหา)
DEFAULT_K = 8 # จำนวนผลลัพธ์เริ่มต้นที่จะดึงกลับมาจากการค้นหา (เช่น จาก Vector Store)
