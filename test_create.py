from loader import load_document
from splitter import split_documents
from vectorstore import create_vector_store, save_vector_store

docs = load_document()
all_splits = split_documents(docs)
vector_store = create_vector_store(all_splits)

if vector_store:
    print("SUCCESS: Vector store created")
    save_vector_store(vector_store)
    print("SUCCESS: Vector store saved")
else:
    print("FAILED: Vector store is None")