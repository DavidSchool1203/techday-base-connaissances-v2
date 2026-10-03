---
title: Journal du projet
status: active
last-reviewed: 2026-10-03
sources: ["supports du TechDay", "base de connaissance.csv"]
tags: [techday, suivi]
---

# Journal

## 2026-10-03

- Projet Supabase créé et déclaré en bonne santé sur la capture d'écran.
- Supports lus : diaporama, modèle `AGENTS.md` et CSV de 147 enregistrements.
- Socle local préparé : règles, suivi et copie locale du CSV.
- Script d'import et schéma SQL préparés localement, sans modification de Supabase.
- L'utilisateur a précisé que GitHub doit conserver chaque version terminée du code. La mise en ligne d'un site et la clé API attendront.
- Prochaine étape : choisir le compte GitHub, créer le dépôt, enregistrer la version initiale, puis exécuter le schéma dans Supabase et importer les données.
- La table existante `base_connaissances` a été vérifiée : 147 lignes et RLS active.
- L'application ne doit pas demander de connexion. La table et le chatbot seront donc accessibles en lecture depuis l'application HTML locale, sans possibilité d'écriture.
- La fonction Supabase `chat-with-knowledge` cherche au plus 12 fiches locales pertinentes et utilise la clé Gemini `API_1` stockée dans les secrets Supabase. Les URL ne sont jamais envoyées à Gemini.
- Test validé sans connexion : les 147 fiches sont affichées et le chatbot répond à une question sur Blender avec la fiche source correspondante. Le modèle utilisé est `gemini-3.5-flash`.
- L'historique a été enregistré et envoyé vers `DavidSchool1203/techday-base-connaissances-v2` après connexion de GitHub CLI au compte `DavidSchool1203`.
