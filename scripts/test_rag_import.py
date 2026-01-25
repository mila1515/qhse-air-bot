import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.rag.pipeline.rag_chain import rag_pipeline
    print("Import successful")
    print(f"LLM initialized? {rag_pipeline.llm is not None}")
except Exception as e:
    print(f"Import failed: {e}")
