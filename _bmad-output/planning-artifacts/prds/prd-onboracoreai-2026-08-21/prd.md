---
title: "Product Requirements Document (PRD) - Onbora Core IA"
status: draft
created: 2026-08-21
updated: 2026-08-21
project: onboracoreai
context: "Orange Summer Challenge - Moteur IA Multi-Agents B2B (Copilote Terrain & Qualification Inbound)"
author: "Steve & BMad Master PM"
---

# PRD: Onbora Core IA

## 0. Document Purpose

Ce document spécifie les exigences fonctionnelles et techniques détaillées du **Core IA Onbora**, un moteur d'intelligence artificielle backend modulaire, multi-agents et multi-LLM développé dans le cadre de l'**Orange Summer Challenge**. 

Ce PRD s'adresse à l'équipe de développement, aux architectes système, et aux parties prenantes du projet. Il définit le périmètre **strictement centré sur le Core IA** (moteur d'orchestration, agents, API FastAPI, RAG hybride, mémoire court/long terme, connecteurs MCP, contrats de données). Les applications clientes (Mobile Flutter, Web React, Backend Django) sont traitées ici comme des consommateurs de l'API.

## 0.1 Existing Implementation Baseline

This project is brownfield. As of 2026-08-23, the repository contains a
Python/Strands/Gemini POC with a CLI assistant, Streamlit interface, supervisor,
researcher delegation, structured commercial report generation, and optional
Django report POST. These components are discovery and migration inputs only.
They do not satisfy a functional requirement unless their corresponding epic
acceptance criteria and automated tests are met.

The MVP target remains the FastAPI-based Onbora Core IA defined in this PRD.
Before implementing a target component, the team must classify the related POC
code as retain, adapt, replace, or retire and preserve a traceable rationale.

---

## 1. Vision

**Onbora Core IA** est le cerveau décisionnel et conversationnel conçu pour maximiser l'efficacité de la force de vente et la qualification des prospects pour les offres et services **Orange B2B**.

Le produit résout deux défis fondamentaux :
1. **Pendant le rendez-vous commercial terrain** : transformer une conversation orale en opportunité de vente immédiate grâce à un copilote ultra-faible latence qui pousse des recommandations d'offres Orange ciblées et génère automatiquement le compte-rendu d'activité pour le CRM.
2. **Sur les canaux digitaux entrants (Inbound)** : convertir les visiteurs professionnels en leads qualifiés grâce à un conseiller virtuel expert du catalogue Orange B2B, capable de transmettre des fiches de synthèse prêtes pour les Key Account Managers (KAM).

L'architecture repose sur 4 piliers technologiques :
* Une **orchestration multi-agents dynamique** (*Agent Registry Pattern*).
* Un **RAG hybride** (vectoriel dense + recherche textuelle BM25) sur la documentation et le catalogue Orange B2B.
* Une **double gestion de mémoire** (mémoire de session avec compression automatique de contexte + mémoire d'entité long terme).
* Une interopérabilité standardisée via des connecteurs **Model Context Protocol (MCP)**.

---

## 2. Utilisateurs Cibles & Parcours

### 2.1 Personas & Jobs To Be Done (JTBD)

* **Le Commercial Terrain Orange B2B (Amadou)** :
  * *JTBD Fonctionnel* : Obtenir instantanément la bonne offre Orange et le bon argument face aux besoins exprimés par le prospect sans chercher dans un catalogue complexe.
  * *JTBD Émotionnel* : Rester concentré sur l'écoute active et la relation humaine sans stresser sur la prise de note ni sur le compte-rendu post-visite.
* **Le Prospect Professionnel Inbound (Sarah, DG d'une PME)** :
  * *JTBD* : Décrire ses problématiques télécoms/cloud simplement et obtenir une recommandation d'offre claire et sans jargon.
* **Le Key Account Manager / Superviseur des Ventes (Marc)** :
  * *JTBD* : Recevoir des fiches de prospects et des rapports de visite 100% exploitables, quantifiés et intégrés dans le CRM Django sans ressaisie manuelle.

---

### 2.2 Key User Journeys (UJ)

#### **UJ-1 : Visite terrain avec Copilote et validation de Carte Conseil**
* **Contexte & Acteur** : Amadou (Commercial) est en rdv chez un client B2B. Son application mobile Flutter est active en mode enregistrement (transcription audio au fil de l'eau).
* **Entrée** : L'app Flutter ouvre un flux SSE vers `POST /api/v1/copilot/stream`.
* **Déroulement** :
  1. Le prospect déclare : *"Nos équipes sur site distant se plaignent de coupures internet récurrentes et notre VPN saute."*
  2. Le Core IA reçoit le chunk textuel, le RAG hybride extrait l'offre Orange correspondante, et pousse une **Carte Conseil** en SSE : *« Proposer Orange Fibre Pro 1 Gbps avec Option Backup 4G automatique + VPN Managé »*.
  3. Amadou voit la carte s'afficher sur son smartphone sans notification sonore intrusive, et clique sur **[Accepter]**.
  4. L'acceptation est transmise à `POST /api/v1/copilot/feedback` pour orienter la suite du contexte.
* **Climax** : Amadou place l'argument Orange immédiatement avec assurance ; le prospect valide l'intérêt pour un devis.
* **Résolution** : En fin de rdv, Amadou clique sur "Terminer la visite". Le sous-agent `conversation_reporter` compile l'échange et pousse le JSON validé dans le CRM Django.

#### **UJ-2 : Préparation en amont d'une visite (Company Recon)**
* **Contexte & Acteur** : Amadou prépare sa visite 15 minutes avant le rendez-vous.
* **Déroulement** :
  1. Il saisit le nom de l'entreprise cible dans l'application.
  2. L'agent `company_researcher` via le connecteur MCP Web Recon recherche les informations publiques (secteur, taille, technologies, actualités, présence locale).
  3. L'agent synthétise une fiche "Brief Express" mettant en avant les besoins télécoms/IT probables de ce profil d'entreprise.
* **Résolution** : Amadou aborde la réunion avec une connaissance préalable du contexte de son prospect.

#### **UJ-3 : Diagnostic Inbound & Transmission KAM**
* **Contexte & Acteur** : Sarah (Prospect) discute avec le Chatbot Onbora sur le portail Web.
* **Déroulement** :
  1. Sarah expose ses besoins en connectivité et flotte mobile pour 25 collaborateurs.
  2. L'agent `lead_qualifier` mène l'échange, affine les contraintes techniques et budgétaires, et présente les offres Orange adaptées issues du RAG.
  3. Le sous-agent génère un rapport de qualification complet avec un score de maturité (ex: 88/100).
* **Résolution** : Le rapport est injecté dans le CRM via le connecteur MCP CRM, et le KAM Marc est notifié pour le rappel commercial.

---

## 3. Glossaire

* **Core IA** : L'ensemble du backend d'intelligence artificielle (API FastAPI, orchestrateur, agents, RAG, mémoire).
* **Copilote Temps Réel** : Sous-agent spécialisé dans l'analyse au vol de fragments de transcription et la génération de recommandations discrètes.
* **Carte Conseil (`SuggestionCard`)** : Unité d'information poussée au commercial contenant : le besoin identifié, l'offre Orange suggérée, l'argumentaire clé et un indice de confiance.
* **RAG Hybride** : Mécanisme de recherche combinant la recherche sémantique vectorielle (dense embeddings) et la recherche textuelle exacte (sparse BM25/lexicale).
* **Working Memory (Mémoire de Session)** : Mémoire vive (RAM/Redis) conservant le fil de la session en cours avec compression périodique.
* **Entity Memory (Mémoire Long Terme)** : Base de faits persistants (SQLite/PostgreSQL) sur les entreprises, contacts et antécédents de visites.
* **Connecteur MCP (Model Context Protocol)** : Interface standardisée permettant aux agents d'interagir avec les outils externes (CRM, Web Search, Catalogue RAG).
* **`ConversationReport`** : Contrat de données Pydantic formalisant le compte-rendu complet d'un échange commercial.

---

## 4. Spécifications des Fonctionnalités (Features)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         ONBORA CORE IA ENGINE                            │
├──────────────────────────────────────────────────────────────────────────┤
│ 1. API GATEWAY (FastAPI)                                                 │
│    - Endpoints REST • SSE Streaming • WebSockets                         │
├──────────────────────────────────────────────────────────────────────────┤
│ 2. DYNAMIC ORCHESTRATOR & AGENT REGISTRY                                 │
│    - Multi-LLM Router (Gemini, Groq, OpenAI, Claude)                    │
├──────────────────┬──────────────────┬─────────────────┬──────────────────┤
│ 3. COPILOTE      │ 4. RAG HYBRIDE   │ 5. MÉMOIRE      │ 6. CONNECTEURS   │
│    TEMPS RÉEL    │    CATALOGUE     │    DOUBLE NIVEAU│    MCP           │
│  - Flux STT      │  - Dense Vector  │  - Session RAM/ │  - MCP CRM       │
│  - Détection     │  - BM25 Mots-clés│    Redis + Comp.│  - MCP Web Recon │
│  - Cartes Conseils  - PDF/Markdown  │  - Entity SQL/PG│  - MCP RAG Docs  │
└──────────────────┴──────────────────┴─────────────────┴──────────────────┘
```

### 4.1 Feature 1 : API Gateway & Protocoles d'Interaction
**Description :** Exposition de tous les services du Core IA via une API FastAPI asynchrone, sécurisée et documentée (Swagger / OpenAPI).

* **FR-1 : Endpoint Streaming Copilote (SSE)**
  * *Comportement* : `POST /api/v1/copilot/stream` reçoit des fragments de texte et diffuse en streaming les événements de statut et les `SuggestionCard` dès leur détection.
  * *Testabilité* : L'événement SSE `suggestion_card` est émis en moins de 1,5s après l'envoi d'un chunk contenant une intention d'achat.
* **FR-2 : Endpoint Feedback Commercial**
  * *Comportement* : `POST /api/v1/copilot/feedback` reçoit `{ "suggestion_id": "...", "status": "accepted|rejected", "reason": "..." }` et met à jour la mémoire de session.
* **FR-3 : Endpoint Rapport de Visite**
  * *Comportement* : `POST /api/v1/reports/generate` prend un transcript ou un `session_id` et retourne un objet JSON strictement validé selon `ConversationReport`.
* **FR-4 : Endpoint Recherche Entreprise**
  * *Comportement* : `POST /api/v1/company/research` retourne la fiche synthétique d'une entreprise à partir de son nom et/ou site web.
* **FR-5 : Endpoint Chatbot Inbound**
  * *Comportement* : `POST /api/v1/chat/message` gère les tours de parole du prospect web avec streaming de réponse.

---

### 4.2 Feature 2 : Orchestrateur Central & Agent Registry
**Description :** Système de routage modulaire permettant d'enregistrer, configurer et invoquer des sous-agents dynamiquement.

* **FR-6 : Découplage Multi-LLM par Agent**
  * *Comportement* : L'orchestrateur permet d'assigner des modèles différents par agent (ex: Groq/Gemini Flash pour `realtime_copilot` pour minimiser la latence ; Gemini Pro/GPT-4o pour `conversation_reporter` pour la rigueur du schéma).
* **FR-7 : Agent Registry Extensible**
  * *Comportement* : Tout nouveau sous-agent s'enregistre via une classe standard définissant son prompt, ses outils MCP, son schéma d'entrée et sa sortie structurée.

---

### 4.3 Feature 3 : Copilote Terrain Ultra Temps Réel
**Description :** Analyse à faible latence des fragments de texte pour assister le commercial en direct sans surcharge cognitive.

* **FR-8 : Filtrage et Seuil de Déclenchement (Anti-Spam)**
  * *Comportement* : Le copilote analyse les chunks mais ne génère une `SuggestionCard` que si le score de confiance dépasse un seuil paramétrable (ex: >= 0.75) ou si une objection majeure est identifiée.
* **FR-9 : Structure de la Carte Conseil**
  * *Comportement* : Chaque carte conseil contient obligatoirement : `need_detected`, `suggested_offer`, `pitch_argument`, `confidence_score` et `card_id`.

---

### 4.4 Feature 4 : Moteur RAG Hybride & Catalogue Orange B2B
**Description :** Système d'indexation et d'interrogation documentaire multi-sources assurant la conformité aux offres officielles Orange.

* **FR-10 : Indexation Multi-Formats**
  * *Comportement* : Le moteur ingère des fichiers PDF, Markdown, JSON (fiches offres, grilles tarifaires, argumentaires, FAQ).
* **FR-11 : Recherche Hybride (Dense + Sparse)**
  * *Comportement* : Toute requête combine la recherche vectorielle sémantique (embeddings Gemini / OpenAI / FastEmbed) et la recherche lexicale BM25 pour garantir l'exactitude des noms d'offres et codes produits.
* **FR-12 : Injection Contextuelle RAG**
  * *Comportement* : Les chunks documentaires les plus pertinents (Top-K) sont automatiquement injectés dans le prompt du sous-agent requérant.

---

### 4.5 Feature 5 : Double Système de Mémoire
**Description :** Gestion différenciée de la mémoire vive de session et de la mémoire d'entité long terme.

* **FR-13 : Mémoire de Session avec Compression Automatique**
  * *Comportement* : La session active conserve l'historique en mémoire vive (RAM / Redis). Si la conversation dépasse un seuil de tokens (ex: réunion de plus de 45 minutes), un sous-agent de compression résume automatiquement les segments anciens tout en conservant les faits et cartes validées.
* **FR-14 : Mémoire Long Terme des Entités (Entreprises & Contacts)**
  * *Comportement* : Les faits durables (nom de l'entreprise, décisionnaires, solutions déjà installées, échéances de contrats concurrents) sont persistés dans la base (SQLite en dev / PostgreSQL en prod) et réinjectés lors des futures interactions avec cette entreprise.

---

### 4.6 Feature 6 : Connecteurs & Architecture MCP (Model Context Protocol)
**Description :** Découplage complet des outils et sources de données externes via le standard MCP.

* **FR-15 : Serveur MCP CRM / Django**
  * *Comportement* : Expose les outils standardisés pour : `get_client_history`, `create_lead`, `update_client_note`, `save_conversation_report`.
* **FR-16 : Serveur MCP Web Recon**
  * *Comportement* : Expose les outils de recherche web et scraping de données d'entreprise pour `company_researcher`.
* **FR-17 : Serveur MCP RAG Catalogue**
  * *Comportement* : Expose l'outil `search_orange_catalog(query, category, limit)` permettant à n'importe quel sous-agent d'interroger la base documentaire Orange B2B.

---

### 4.7 Feature 7 : Rapporteur Commercial & Validation Pydantic
**Description :** Transformation déterministe d'une conversation en synthèse structurée pour le CRM.

* **FR-18 : Contrat Pydantic Strict (`ConversationReport`)**
  * *Comportement* : Le rapport contient obligatoirement : `summary`, `key_points`, `customer_needs`, `pain_points`, `objections`, `recommended_next_actions`, `interest_level` (unknown, low, medium, high), `lead_status` (new, qualified, nurturing, won, lost), `qualification_score` (0-100), `missing_information`.
* **FR-19 : Tolérance aux Pannes & Retry de Format**
  * *Comportement* : En cas d'erreur de parsing JSON, le système réexécute une passe d'auto-correction avant de retourner une erreur.

---

## 5. Non-Functional Requirements (NFR)

* **NFR-1 (Latence Copilote)** : Le temps de réponse de bout en bout pour émettre une `SuggestionCard` via SSE ne doit pas dépasser **1500 ms** à compter de la réception du chunk textuel.
* **NFR-2 (Robustesse JSON)** : 100% des sorties du rapporteur commercial doivent valider le modèle Pydantic sans exception non gérée.
* **NFR-3 (Scalabilité & Modularité)** : L'ajout d'un nouveau sous-agent ou d'un nouveau serveur MCP ne doit nécessiter aucune modification du code de l'API Gateway.
* **NFR-4 (Multi-LLM Fallback)** : En cas d'indisponibilité ou d'erreur de quota d'un fournisseur LLM principal (ex: Gemini), le système peut basculer automatiquement sur un fournisseur de secours configuré.
* **NFR-5 (Consommation de Mémoire)** : La compression de contexte doit maintenir la taille du prompt actif sous la barre des 8 000 tokens quelle que soit la durée du rendez-vous.

---

## 6. Non-Goals (Explicites pour le Core IA)

* **NON-GOAL 1** : Le Core IA ne développe pas d'interfaces graphiques (l'application Flutter et l'application Web sont gérées par des projets clients distincts).
* **NON-GOAL 2** : Le Core IA ne réalise pas de transcription audio Speech-to-Text directe dans le MVP (il consomme des flux de texte pré-transcrits envoyés par les clients).
* **NON-GOAL 3** : Le Core IA ne gère pas de système de facturation ou de signature électronique de contrats Orange B2B dans la V1.

---

## 7. Délimitation du Périmètre (Scope MVP vs Futur)

### ✅ Scope MVP (Orange Summer Challenge) :
* Serveur FastAPI avec routes REST, SSE pour le streaming temps réel et WebSockets.
* Orchestrateur modulaire avec support Multi-LLM (Gemini par défaut + adaptateurs).
* 5 Sous-agents opérationnels : `realtime_copilot`, `catalog_recommender`, `company_researcher`, `conversation_reporter`, `lead_qualifier`.
* Moteur RAG Hybride (Dense + BM25) indexant le catalogue d'offres Orange B2B (JSON/Markdown/PDF).
* Double niveau de mémoire : Session RAM/Redis avec compression de contexte + SQLite/PostgreSQL pour les entités durables.
* 3 Serveurs / Connecteurs MCP intégrés : MCP CRM Django, MCP Web Recon, MCP RAG Catalogue.
* Suite de tests unitaires et d'intégration automatisée validant les flux de bout en bout.

### ⏳ Scope V2 / V3 :
* Endpoint d'ingestion audio direct avec transcription STT hébergée.
* Synthèse vocale (TTS) pour retour audio oreillette.
* Connecteurs MCP supplémentaires pour d'autres CRM du marché (Salesforce, HubSpot).

---

## 8. Critères de Succès & Métriques

* **SM-1 (Vitesse Copilote)** : 95% des cartes conseils générées en < 1.5s (*Valide FR-1, FR-8, NFR-1*).
* **SM-2 (Précision RAG)** : > 90% des offres Orange recommandées correspondent exactement aux besoins du prospect (*Valide FR-11, FR-17*).
* **SM-3 (Taux de Succès des Rapports)** : 100% des requêtes de rapport aboutissent à un JSON valide injecté sans rejet CRM (*Valide FR-3, FR-18, NFR-2*).
* **SM-C1 (Contre-métrique Pertinence)** : Le taux de cartes conseils rejetées par le commercial (`POST /copilot/feedback`) ne doit pas dépasser 20% (garantit de ne pas surcharger le commercial avec des suggestions hors-sujet).

---

## 9. Open Questions & Prochaines Étapes

1. **Question Ouverte 1** : Quel est le jeu de données initial exact des offres Orange B2B (combien d'offres au démarrage pour l'Orange Summer Challenge) ? *(Sera injecté dans le dossier `data/catalog/`)*.
2. **Question Ouverte 2** : Quels sont les champs exacts attendus par le backend Django pour la synchronisation CRM ? *(Le modèle `ConversationReport` actuel couvre l'essentiel et pourra être ajusté)*.

### Handoff vers l'Architecture BMad (`bmad-architecture`) :
Le PRD est complet, validé et prêt à servir de contrat fonctionnel pour la conception de l'architecture logicielle (`bmad-architecture`).
