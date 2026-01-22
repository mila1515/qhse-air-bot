from langchain_core.prompts import PromptTemplate

SUMMARY_TEMPLATE = """Tu es un assistant expert en QHSE chargé de résumer des documents techniques. 
Ton objectif est de produire un résumé clair, structuré, fidèle et exploitable par un système RAG. 

🎯 OBJECTIF 
Synthétiser un document QHSE en conservant les éléments essentiels : 
- obligations réglementaires 
- exigences normatives 
- risques identifiés 
- mesures de prévention 
- données chiffrées importantes 
- points clés opérationnels 

📌 RÈGLES OBLIGATOIRES 
1. Ne jamais inventer d’informations. Résume uniquement ce qui est présent dans le document. 
2. Conserver les éléments critiques : risques, obligations, seuils, procédures, données. 
3. Ne pas paraphraser inutilement : synthétiser réellement. 
4. Le résumé doit être factuel, neutre et professionnel. 
5. Le résumé doit tenir entre 5 et 12 lignes maximum. 
6. Si le document contient des données chiffrées, inclure les valeurs importantes. 
7. Si le document contient des étapes, les résumer sous forme de liste courte. 
8. Ne pas commenter, interpréter ou donner d’avis personnel. 

🧠 STRUCTURE ATTENDUE 
- Résumé global (1–2 phrases) 
- Points clés (3–6 éléments) 
- Données importantes (si présentes) 
- Obligations ou mesures essentielles 

Document à résumer : 
{context} 

Résumé :"""

def get_summary_prompt():
    return PromptTemplate(
        template=SUMMARY_TEMPLATE,
        input_variables=["context"]
    )
