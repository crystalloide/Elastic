___

1. Structure de dossiers recommandée sur le poste stagiaire

Avant de démarrer l'environnement, créez l'arborescence suivante dans votre dossier de TP :
TP/
├── docker-compose.yml
├── data/
│   └── access.log            # Fichier de logs Apache Combined Format pour les Ateliers 2 & 3
└── logstash/
    └── pipeline/
        └── apache_pipeline.conf  # Pipeline Logstash pour l'Atelier 3

___

2. Identifiants et ports configurés :

- Elasticsearch : https://localhost:9200   Utilisateur : elastic  Mot de passe : elasticpassword

- Kibana : http://localhost:5601  Connecté automatiquement à Elasticsearch via le compte kibana_system / kibanapassword

- Logstash :
	- Port Beats / Filebeat : 5044
	- Port HTTP Ingestion : 8080

___

3. Commandes de démarrage et validation (Atelier 1)

Lancer la stack en arrière-plan :

docker compose up -d


Vérifier l'état de santé du cluster (Atelier 1) : 
 
 
curl -k -u elastic:elasticpassword https://localhost:9200/_cluster/health


Lister les nœuds du cluster via l'API _cat :  


curl -k -u elastic:elasticpassword "https://localhost:9200/_cat/nodes?v"


Accéder à Kibana Dev Tools :  
- Ouvrez http://localhost:5601 dans votre navigateur.  
- Connectez-vous avec elastic / elasticpassword
- Allez dans Management > Dev Tools pour exécuter les requêtes Query DSL et ES|QL


___

4. Génération de logs fictives :

Exécution et intégration :

Exécutez le script generate_logs.py depuis la racine de votre projet TP :

python3 generate_logs.py

Le fichier data/access.log généré sera immédiatement lisible par Logstash grâce au montage de volume défini dans docker-compose.yml (./data:/data:ro).  

Dans Logstash, le filtre grok avec le pattern %{COMBINEDAPACHELOG} extraira automatiquement tous les champs requis pour constituer la Data View et le Dashboard Kibana.  




___


#### Annexe : 

Dans l'écosystème Elasticsearch 8.x, 
il existe deux approches pour gérer le démarrage du cluster et la connexion de Kibana lors des ateliers :

### Option A : Mots de passe prédéfinis (Approche intégrée dans le docker-compose.yml fourni)

C'est l'approche la plus fluide pour une formation de 2 jours 
afin d'éviter que les stagiaires ne perdent du temps à chercher des clés dans les logs Docker.

Dans le fichier docker-compose.yml fourni précédemment : 

- Mot de passe elastic : Défini explicitement à elasticpassword via la variable ELASTIC_PASSWORD

- Jeton d'enrollment Kibana : Contourné grâce au conteneur d'initialisation setup_kibana_pass qui configure le mot de passe kibana_system et le transmet à Kibana via les variables d'environnement.

Résultat pour les stagiaires : 
Dès que docker compose up -d est terminé, Kibana est déjà connecté à Elasticsearch 
et accessible sur http://localhost:5601 sans réclamer de jeton d'enrollment (enrollment token).


### Option B : Mode standard Elastic 8 (Génération automatique des identifiants & jetons)

Si vous souhaitez faire manipuler aux stagiaires le comportement natif d'Elasticsearch 8 
(génération automatique des certificats, du mot de passe elastic et du token Kibana au premier démarrage), 

voici le script bash d'initialisation/extraction à fournir aux stagiaires 
ou à exécuter en amont :

Script d'extraction/génération : init-cluster.sh

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



### Récapitulatif pour l'animation de l'Atelier 1

Élément										Commandes Utiles pour le Formateur / Stagiaires

Générer un jeton Kibana à la demande		docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana

Réinitialiser le mot de passe elastic		docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic

Vérifier le statut du cluster avec curl		curl -k -u elastic:elasticpassword https://localhost:9200/_cluster/health?pretty

Consulter les logs de démarrage master		docker logs elasticsearch | grep -i "selected-as-master"









