-- Dell V4 owner OTP/link single-use authorization ledger, isolated from other projects.
-- No live release authority is enabled by installing this table.
-- The API must be a narrowly scoped Edge function with server-owned service credentials.
create table if not exists public.matrix_v4_owner_challenges (
  id uuid primary key,
  owner_uid uuid not null,
  host_id text not null default 'dell-linux'
    check (host_id = 'dell-linux'),
  project_name text not null default 'matrix_dev_manager'
    check (project_name = 'matrix_dev_manager'),
  source_commit text not null check (source_commit ~ '^[0-9a-f]{40}$'),
  manifest_sha256 text not null check (manifest_sha256 ~ '^[0-9a-f]{64}$'),
  nonce_sha256 text not null check (nonce_sha256 ~ '^[0-9a-f]{64}$'),
  status text not null default 'pending'
    check (status in ('pending','consumed','expired')),
  created_at timestamptz not null default now(),
  expires_at timestamptz not null
    check (expires_at > created_at and expires_at <= created_at + interval '5 minutes'),
  consumed_at timestamptz,
  consumed_method text check (consumed_method in ('otp','link')),
  signing_receipt_sha256 text check (signing_receipt_sha256 ~ '^[0-9a-f]{64}$'),
  check (
    (status = 'pending' and consumed_at is null and consumed_method is null) or
    (status = 'expired' and consumed_at is null and consumed_method is null) or
    (status = 'consumed' and consumed_at is not null and consumed_method is not null)
  )
);
alter table public.matrix_v4_owner_challenges enable row level security;
alter table public.matrix_v4_owner_challenges force row level security;
revoke all on table public.matrix_v4_owner_challenges from public, anon, authenticated;
grant select, insert, update on table public.matrix_v4_owner_challenges to service_role;
create index if not exists matrix_v4_owner_challenges_owner_created
  on public.matrix_v4_owner_challenges(owner_uid,created_at desc);
create index if not exists matrix_v4_owner_challenges_pending
  on public.matrix_v4_owner_challenges(owner_uid,expires_at)
  where status='pending';
-- No PUBLIC / anon / authenticated policies, no SECURITY DEFINER RPC.
-- A status update WHERE status=pending AND expires_at>now() is atomic.
-- The separate signer MUST only run after Auth ownership validation and
-- exactly one returned row from that update.
