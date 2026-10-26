-- Auth owner enrollment for Dell V4 only. Identity record is NOT release signing authority.
-- Deliberately no email address or UID in version-controlled source.
create table if not exists public.matrix_v4_owner_registry (
  host_id text primary key check (host_id='dell-linux'),
  project_name text not null check (project_name='matrix_dev_manager'),
  owner_uid uuid not null unique references auth.users(id) on delete restrict,
  owner_email text not null check (owner_email=lower(owner_email) and position('@' in owner_email)>1),
  identity_enrolled boolean not null default true,
  release_signing_enabled boolean not null default false
    check (release_signing_enabled=false),
  enrolled_at timestamptz not null default now()
);
alter table public.matrix_v4_owner_registry enable row level security;
alter table public.matrix_v4_owner_registry force row level security;
revoke all on public.matrix_v4_owner_registry from PUBLIC, anon, authenticated;
grant select on public.matrix_v4_owner_registry to service_role;
-- Enrollment and any future revocation remain authenticated owner-admin migrations,
-- not a publicly callable API or a worker-owned SQL mutation.
