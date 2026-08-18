#!/bin/bash
echo "=== 1. Attente du démarrage complet d'Elasticsearch ==="
until curl -s -k https://localhost:9200 -u elastic:elasticpassword > /dev/null; do
    echo "En attente d'Elasticsearch..."
    sleep 3
done

echo -e "\n=== 2. Génération d'un jeton d'enrollment Kibana ==="
TOKEN=$(docker exec -ti elasticsearch /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana)
echo "Jeton d'enrollment Kibana :"
echo "$TOKEN"

echo -e "\n=== 3. Réinitialisation du mot de passe 'elastic' (si besoin) ==="
# Pour réinitialiser interactivement ou récupérer le passe
docker exec -ti elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic -b -s

echo -e "\n=== 4. Vérification de l'accès TLS avec curl ==="
curl -k -u elastic:elasticpassword https://localhost:9200/_cluster/health?pretty