import time
import os
from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway
from src.config import get_settings
from src.monitoring.logger import logger

# Registre unique pour les métriques ETL
registry = CollectorRegistry()

# 1. Métriques de Succès/Échec
ETL_LAST_RUN_SUCCESS = Gauge(
    'etl_last_run_success_timestamp', 
    'Timestamp du dernier succès ETL (Unix)', 
    registry=registry
)

ETL_ERROR_COUNT = Counter(
    'etl_error_count_total', 
    'Nombre total d\'erreurs ETL', 
    ['source'], # Labels: waqi, inrs, cdtn, aria
    registry=registry
)

# 2. Métriques de Volume (Lignes traitées)
ETL_PROCESSED_ROWS = Counter(
    'etl_processed_rows_total', 
    'Nombre de lignes traitées/insérées', 
    ['source', 'step'], # step: collect, transform, load
    registry=registry
)

# 3. Métriques Métier (Qualité Air)
# On utilise un Gauge pour stocker la dernière valeur connue
AIR_QUALITY_INDEX = Gauge(
    'air_quality_index_value', 
    'Indice de qualité de l\'air (AQI) par ville', 
    ['ville'], 
    registry=registry
)

# 4. Métriques RAG (Performance & Fallback)
RAG_QUERY_LATENCY = Gauge(
    'rag_query_latency_seconds',
    'Temps de réponse du RAG en secondes',
    registry=registry
)

RAG_FALLBACK_COUNT = Counter(
    'rag_fallback_activation_total',
    'Nombre de bascules sur le LLM de secours',
    registry=registry
)

def push_metrics():
    """Pousse les métriques vers la Pushgateway (si configurée)"""
    # URL de la Pushgateway (par défaut localhost:9091)
    gateway_url = os.getenv("PUSHGATEWAY_URL", "localhost:9091")
    
    try:
        push_to_gateway(
            gateway=gateway_url, 
            job='qhse_etl_job', 
            registry=registry
        )
        logger.info(f"📈 Métriques poussées vers Pushgateway ({gateway_url})")
    except Exception as e:
        # En local sans docker, ça échouera souvent, on log juste un warning
        logger.warning(f"⚠️ Impossible de pousser les métriques vers Pushgateway: {e}")

def record_etl_success():
    """Enregistre le succès de l'ETL"""
    ETL_LAST_RUN_SUCCESS.set_to_current_time()

def record_etl_error(source: str):
    """Incrémente le compteur d'erreurs"""
    ETL_ERROR_COUNT.labels(source=source).inc()

def record_processed_rows(source: str, step: str, count: int):
    """Enregistre le nombre de lignes traitées"""
    ETL_PROCESSED_ROWS.labels(source=source, step=step).inc(count)

def update_aqi_gauge(ville: str, aqi_value: int):
    """Met à jour la jauge AQI pour une ville"""
    try:
        if aqi_value is not None:
            AIR_QUALITY_INDEX.labels(ville=ville).set(aqi_value)
    except Exception:
        pass
