# TechDay — base de connaissances

Application HTML locale connectée au projet Supabase `TechDay 03.10.2026`.

## Utiliser l'application

1. Ouvrir `index.html` dans un navigateur.
2. Consulter ou rechercher les 147 fiches dans l'onglet **Base de connaissances**.
3. Poser une question dans l'onglet **Chatbot**. La fonction Supabase utilise la clé Gemini `API_1` stockée dans les secrets du projet.

## Sécurité

Le navigateur contient uniquement l'URL du projet et la clé Supabase `publishable`. La clé Gemini reste dans Supabase. Les fiches et le chatbot sont volontairement accessibles sans connexion, en lecture seule.

## Fichiers importants

- `index.html` : interface locale.
- `supabase/owner_access.sql` : accès sécurisé à la table existante.
- `supabase/chat-with-knowledge.ts` : chatbot exécuté par Supabase.
- `AGENTS.md` : mémoire et règles de travail hors ligne.
