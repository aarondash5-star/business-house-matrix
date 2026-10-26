-- Guarantee one pending owner release challenge at a time; expired rows are
-- changed to status=expired by the gated Edge function before a fresh request.
create unique index if not exists matrix_v4_owner_pending_once
 on public.matrix_v4_owner_challenges(owner_uid)
 where status='pending';
