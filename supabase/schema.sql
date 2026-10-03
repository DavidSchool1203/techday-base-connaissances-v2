-- Socle du TechDay. À exécuter une fois dans le SQL Editor du projet Supabase.
-- La table reste protégée par RLS sans politique d'accès publique.

create extension if not exists vector with schema extensions;

create table if not exists public.knowledge_items (
    source_row integer primary key,
    nom text,
    note_alex text,
    texte text,
    url text,
    date_maj_n8n text,
    etiquettes text,
    enriched_title text,
    enriched_summary text,
    enriched_tags text[],
    enrichment_source_url text,
    enrichment_status text not null default 'pending'
        check (enrichment_status in ('pending', 'done', 'error', 'skipped')),
    enriched_at timestamptz,
    created_at timestamptz not null default now()
);

alter table public.knowledge_items enable row level security;

