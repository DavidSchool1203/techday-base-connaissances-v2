# Règles de travail du projet TechDay

Ce fichier adapte le modèle fourni pour le cours à notre projet Codex.

## Communication

- Expliquer les manipulations en français, simplement et étape par étape.
- Vérifier les résultats avant de dire qu'une étape est terminée.
- Signaler clairement ce qui reste à faire ou à décider.

## Code et données

- Conserver le CSV d'origine sans le modifier. Traiter les lignes vides et les champs manquants explicitement.
- Garder les mots de passe et les clés privées dans des fichiers `.env` locaux, jamais dans Git.
- Utiliser la clé Supabase `publishable` pour le navigateur. Ne jamais y placer une clé `secret` ou `service_role`.
- L'application locale est une page `index.html` avec deux onglets : la base de connaissances et le chatbot.
- La clé Gemini `API_1` reste dans les secrets Supabase ; seul le chatbot côté Supabase peut l'utiliser.
- Ne jamais effacer ni réinitialiser la base Supabase sans accord explicite et sauvegarde préalable.

## Git et publication

- Faire des changements compréhensibles et des commits avec un message clair.
- Vérifier l'état Git avant tout envoi. Ne pas forcer un envoi sur `main`.
- Après chaque étape terminée et vérifiée, enregistrer une version du code dans Git et l'envoyer sur le dépôt GitHub choisi par l'utilisateur.
- GitHub conserve l'historique du code. L'application est utilisée localement, sauf demande explicite de publication.

## Mémoire du projet

- Mettre à jour `docs/JOURNAL.md` après les étapes de développement.
- Garder `docs/ROADMAP.md` cohérent avec l'avancement réel.
- Noter les décisions durables dans `docs/DECISIONS.md`.
