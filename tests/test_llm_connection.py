import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.monitoring.logger import logger


def test_connection():
    print("\n🔍 TEST DES CONNEXIONS LLM\n" + "=" * 40)
    load_dotenv()

    print("\n1. [DEEPSEEK]")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if deepseek_key:
        print(f"   ✅ Clé détectée : {deepseek_key[:5]}...{deepseek_key[-3:]}")
        try:
            print("   ⏳ Tentative de connexion...")
            llm = ChatOpenAI(
                model=os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat"),
                api_key=deepseek_key,
                base_url="https://api.deepseek.com",
                temperature=0,
                max_retries=1,
            )
            response = llm.invoke("Bonjour, es-tu opérationnel ? Réponds par 'OUI' seulement.")
            print(f"   🚀 RÉUSSITE ! Réponse : {response.content}")
        except Exception as e:
            print(f"   ❌ ÉCHEC : {e}")
    else:
        print("   ⚪ Clé absente.")

    print("\n2. [OPENAI STANDARD]")
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"   ✅ Clé détectée : {openai_key[:5]}...{openai_key[-3:]}")
        try:
            print("   ⏳ Tentative de connexion...")
            llm = ChatOpenAI(
                model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
                api_key=openai_key,
                temperature=0,
                max_retries=1,
            )
            response = llm.invoke("Bonjour, es-tu opérationnel ? Réponds par 'OUI' seulement.")
            print(f"   🚀 RÉUSSITE ! Réponse : {response.content}")
        except Exception as e:
            print(f"   ❌ ÉCHEC : {e}")
    else:
        print("   ⚪ Clé absente.")

    print("\n" + "=" * 40 + "\n")

