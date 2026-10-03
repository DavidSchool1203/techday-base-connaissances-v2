-- Lecture sans connexion pour l'application HTML locale.
revoke all privileges on table public.base_connaissances from anon, authenticated;
grant select on table public.base_connaissances to anon, authenticated;

drop policy if exists "Le propriétaire peut lire sa base" on public.base_connaissances;
drop policy if exists "La base peut être consultée par l'application locale" on public.base_connaissances;
create policy "La base peut être consultée par l'application locale"
on public.base_connaissances
for select
to anon, authenticated
using (true);
