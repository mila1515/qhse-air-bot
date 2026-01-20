from prometheus_client import Gauge

# Métriques spécifiques à l'API (utilisent le registre par défaut pour être exposées sur /metrics)

DB_CONNECTION_STATUS = Gauge(
    'db_connection_status',
    'Statut de la connexion à la base de données (1 = OK, 0 = Erreur)'
)
