-- Owner-authenticated review feedback for the Dell V4 login UI only.
-- A UI review is NEVER a cryptographic owner release approval.
create table if not exists public.matrix_v4_owner_ui_reviews (
  id bigint generated always as identity primary key,
  owner_uid uuid not null references auth.users(id) on delete restrict,
  host_id text not null check (host_id='dell-linux'),
  project_name text not null check (project_name='matrix_dev_manager'),
  decision text not null check (decision in ('ui_acceptable','needs_changes')),
  notes text not null default '' check (char_length(notes)<=500),
  release_approved boolean not null default false check (release_approved=false),
  reviewed_at timestamptz not null default now()
);
alter table public.matrix_v4_owner_ui_reviews enable row level security;
alter table public.matrix_v4_owner_ui_reviews force row level security;
revoke all on public.matrix_v4_owner_ui_reviews from PUBLIC,anon,authenticated;
grant select,insert on public.matrix_v4_owner_ui_reviews to service_role;
create index if not exists matrix_v4_owner_ui_reviews_recent
 on public.matrix_v4_owner_ui_reviews(owner_uid, reviewed_at desc);
