---
title: "Product Brief - Onbora Core IA"
status: review
created: 2026-08-21
updated: 2026-08-21
project: onboracoreai
context: "Orange Summer Challenge - B2B Sales Enablement & Inbound Lead Qualification"
author: "Steve & BMad Agent"
---

# Product Brief: Onbora Core IA

## 1. Executive Summary

**Onbora Core IA** est le moteur d'intelligence artificielle central, modulaire et hautement évolutif développé pour l'écosystème Onbora dans le cadre de l'**Orange Summer Challenge**. Conçu pour booster l'efficacité commerciale des offres et services **Orange B2B**, il articule deux piliers opérationnels majeurs :

1. **Un Copilote Commercial Terrain en Ultra Temps Réel (App Mobile Flutter)** :
   * L'application mobile Flutter gère la transcription audio (STT via Whisper/micro) et transmet les fragments textuels au fil de l'eau au Core IA.
   * Le Core IA analyse le dialogue à la volée et pousse des **Cartes Conseils discrètes et contextuelles** (détection de besoins, d'objections ou d'opportunités d'up-sell Orange B2B) que le commercial peut **valider ou rejeter** d'un simple geste sans quitter des yeux son client.
   * En fin de visite, le Core IA génère instantanément un **compte-rendu structuré (JSON Django / CRM)** qualifiant la visite (besoins, objections, score de maturité, prochaines actions).
2. **Un Chatbot B2B Intelligent de Qualification Inbound (App Web & Mobile)** :
   * Accueille et dialogue avec les entreprises prospectes cherchant des solutions Orange.
   * Conduit un diagnostic interactif sur mesure, formule des recommandations tirées du catalogue d'offres Orange B2B et génère une fiche de synthèse directement transmise à un **Key Account Manager (KAM)** pour prise en charge prioritaire.

Le système s'appuie sur une architecture **multi-agents orchestrée** (Agent Registry Pattern), un **catalogue d'offres B2B structuré en JSON évolutif**, et une approche **multi-LLM** (Gemini Flash/Pro, OpenAI, Claude, Groq/Mistral) exposée via des endpoints **FastAPI** universels (REST, SSE streaming, WebSockets).

---

## 2. Le Problème & Le Contexte Métier

### Le Contexte : Orange Summer Challenge
La vente d'offres technologiques complexes (Fibre Pro, Connectivité 5G, Cloud, Cybersécurité, Forfaits Flottes, Solutions collaboratives Orange B2B) nécessite une connaissance pointue du catalogue et une réactivité immédiate face aux réticences et besoins du client.

### Les Points de Douleur Résolus :
* **Surcharge cognitive en rendez-vous** : Le commercial doit écouter, argumenter, trouver la bonne offre Orange et négocier en direct. Le Copilote Onbora le soulage en lui suggérant la bonne offre au bon moment.
* **Non-intrusion & Contrôle du commercial** : Pour éviter de spammer le commercial, l'IA n'affiche que des cartes-conseils à haute valeur ajoutée avec validation/rejet manuel (`Thumbs Up / Thumbs Down`).
* **Préparation insuffisante en amont** : Les commerciaux manquent souvent de temps pour se renseigner sur le prospect. L'agent `company_researcher` permet d'obtenir un "Brief Express Entreprise" avant la réunion.
* **Rapports de visite tardifs et incomplets** : Suppression de la saisie manuelle grâce à la génération automatique d'un JSON standardisé injecté dans le backend Django / CRM.
* **Perte de leads entrants B2B** : Les formulaires web statiques ne convertissent pas ; le Chatbot Inbound qualifie dynamiquement et alerte immédiatement le KAM concerné.

---

## 3. Parcours Utilisateurs & Expérience Produit

### Scénario A : Le Rendez-vous Commercial Terrain (App Flutter)

```
[Avant le RDV] ──> Saisie nom entreprise ──> Agent "company_researcher" ──> Fiche Express affichée
       │
[Pendant le RDV] ─> Enregistrement audio + STT Flutter ──> Streaming texte vers Core IA
       │
       ├─────────> Détection Besoin / Objection ──> Push "Carte Conseil" (ex: Fibre Pro + Backup 4G)
       │                                            └──> Action commercial : [Accepter] ou [Rejeter]
       │
[Fin du RDV] ────> Déclenchement Fin de Visite ──> Agent "conversation_reporter"
                                                   └──> Génération JSON Django & Sync CRM
```

### Scénario B : La Qualification Inbound (App Web / Portail)

```
[Prospect B2B sur le site] ──> Dialogue avec le Chatbot Onbora
       │
       ├──> Questions dynamiques de qualification (Secteur, taille, budget, besoins télécoms/cloud)
       ├──> Agent "catalog_recommender" ──> Propositions d'offres Orange B2B personnalisées
       │
[Fin du Chat] ───────────────> Génération Fiche Prospect KAM ──> Notification / Assignation KAM
```

---

## 4. Architecture Multi-Agents & Stratégie Multi-LLM

### Matrice des Sous-Agents Spécialisés

| Agent | Rôle & Responsabilité | Déclenchement | Modèle & Outils |
| :--- | :--- | :--- | :--- |
| **`supervisor`** *(Orchestrateur)* | Supervise les flux, route les messages, gère la session et orchestre les sous-agents. | Central / Tout flux | Gemini 2.5/3 Flash ou GPT-4o-mini |
| **`company_researcher`** | Recherche sur le web et synthétise les infos de l'entreprise (secteur, taille, actus). | **En amont du rdv** (saisie utilisateur) | Gemini + Outil Web Search / API Recon |
| **`realtime_copilot`** | Analyse les fragments de conversation au vol et émet des cartes-conseils ciblées. | **Pendant le rdv** (streaming STT) | Modèle ultra-faible latence (Groq / Gemini Flash) |
| **`catalog_recommender`** | Fait correspondre les besoins détectés avec les références du catalogue Orange B2B. | Appel copilote / chat | JSON Search / Embeddings catalogue B2B |
| **`conversation_reporter`** | Analyse le transcript global et produit le schéma Pydantic `ConversationReport`. | **Fin de visite / Fin de chat** | Gemini Pro / Flash avec validation Pydantic |
| **`lead_qualifier`** | Mène la conversation interactive avec le prospect web pour alimenter la fiche KAM. | Mode Chat Web | Gemini Flash / Claude 3.5 Haiku |

### Gestion du Catalogue Orange B2B
* **Format source** : Fichier structuré `catalog_orange_b2b.json` contenant les offres (ID, catégorie, description, prérequis, arguments de vente, objections courantes et réponses associées).
* **Évolutivité** : Enrichissement transparent sans modification du code des agents.

### Stratégie Multi-LLM
* Configuration découplée via variables d'environnement (`LLM_PROVIDER`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `GROQ_API_KEY`).
* Capacité d'assigner un LLM spécifique par agent selon les exigences de latence (Copilote ultra-rapide) ou de raisonnement (Rapport structuré).

---

## 5. Spécifications des Endpoints API (FastAPI)

Le Core IA est exposé via une API FastAPI asynchrone et documentée :

1. **`POST /api/v1/copilot/stream`** (SSE / WebSocket) :
   * *Entrée* : `{ "session_id": "...", "text_chunk": "...", "speaker": "client|sales" }`
   * *Sortie (Stream)* : Événements SSE contenant soit des métadonnées de statut, soit une `SuggestionCard` :
     ```json
     {
       "type": "suggestion_card",
       "need_detected": "Lenteur connexion internet & coupures régulières",
       "suggested_offer": "Orange Fibre Entreprise Pro 1 Gbps + Option Backup 4G",
       "pitch_argument": "Garantie de temps de rétablissement (GTR 4h) et bascule auto sur réseau mobile en cas de coupure.",
       "estimated_relevance": 0.92
     }
     ```
2. **`POST /api/v1/copilot/feedback`** :
   * Enregistre l'acceptation (`accepted`) ou le rejet (`rejected`) d'une carte conseil par le commercial pour apprentissage contextuel.
3. **`POST /api/v1/company/research`** :
   * *Entrée* : `{ "company_name": "...", "website": "..." }`
   * *Sortie* : Fiche d'identité express (activité, effectif estimé, technologies, enjeux télécoms probables).
4. **`POST /api/v1/reports/generate`** :
   * *Entrée* : `{ "transcript": "...", "session_id": "..." }`
   * *Sortie* : Objet JSON strict conforme à `ConversationReport` (Résumé, besoins, objections, score 0-100, statut lead, next steps).
5. **`POST /api/v1/chat/message`** :
   * Endpoint de discussion pour le Chatbot Inbound avec historique et recommandations d'offres intégrées.
6. **`GET /api/v1/health` & `GET /api/v1/agents`** :
   * Health check et liste des agents et capacités enregistrés.

---

## 6. Délimitation du Périmètre (Scope)

### ✅ Inclus dans le Scope MVP (Orange Summer Challenge) :
* **Core IA FastAPI Engine** avec documentation Swagger interactive.
* **5 Sous-agents opérationnels** : `supervisor`, `company_researcher`, `realtime_copilot`, `catalog_recommender`, `conversation_reporter` (+ persona Chatbot Inbound).
* **Catalogue JSON des offres Orange B2B** intégrant les offres phares (Connectivité Fibre/4G/5G, Cloud, Sécurité, Forfaits Pro).
* **Streaming SSE** pour l'émission des cartes-conseils en direct vers l'application Flutter.
* **Validation Pydantic** stricte pour l'export JSON vers le CRM / Django.
* **Support Multi-LLM** avec Gemini comme moteur par défaut et extensibilité testée.

### ⏳ Hors Scope MVP (Prévu V2 / V3) :
* Transcription audio brute côté serveur (la V1 s'appuie sur le STT côté client Flutter / API externe).
* Synthèse vocale (TTS) avec retour audio dans l'oreillette du commercial.
* Authentification SSO entreprise complexe (OAuth2 basique suffisant pour le MVP).

---

## 7. Critères de Succès & Validation

| Critère | Cible MVP | Méthode de Mesure |
| :--- | :--- | :--- |
| **Latence Carte Conseil** | < 1.5 seconde après réception du chunk textuel clé | Benchmark temps de réponse API SSE |
| **Pertinence Recommandation** | > 85% de suggestions validées par le commercial en test | Taux d'acceptation feedback `POST /copilot/feedback` |
| **Validité JSON Django** | 100% de conformité au schéma Pydantic sans crash | Tests unitaires & intégration Django |
| **Temps de Recherche Entreprise** | < 3 secondes pour produire le Brief Express | Benchmark endpoint `/company/research` |
| **Stabilité Multi-Interfaces** | Intégration fluide démontrée avec Flutter et Web | Démo live Orange Summer Challenge |
