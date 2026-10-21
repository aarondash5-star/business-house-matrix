-- Business House Matrix-only paired research envelope relay (2026-10-21).
-- Deployed once to existing owner-operated Supabase bridge project.
-- Does not alter generic_auto_*, browser PIN*, or Moksha Master tables.
CREATE TABLE IF NOT EXISTS public.bhm_research_devices (
  host_id text PRIMARY KEY CHECK(host_id IN ('mac-linux','dell-linux')),
  verify_key text NOT NULL CHECK(length(verify_key) BETWEEN 40 AND 60),
  box_key text NOT NULL CHECK(length(box_key) BETWEEN 40 AND 60),
  enabled boolean NOT NULL DEFAULT true,
  paired_at timestamptz NOT NULL DEFAULT now(),
  revoked_at timestamptz,
  CONSTRAINT paired_revocation CHECK (NOT enabled OR revoked_at IS NULL)
);
CREATE TABLE IF NOT EXISTS public.bhm_research_jobs (
  id uuid PRIMARY KEY,
  from_host text NOT NULL DEFAULT 'mac-linux' CHECK(from_host='mac-linux'),
  to_host text NOT NULL DEFAULT 'dell-linux' CHECK(to_host='dell-linux'),
  request_box text NOT NULL CHECK(length(request_box) BETWEEN 40 AND 16000),
  response_box text CHECK(response_box IS NULL OR length(response_box) BETWEEN 40 AND 150000),
  state text NOT NULL DEFAULT 'queued' CHECK(state IN ('queued','claimed','completed')),
  claim uuid,
  created_at timestamptz NOT NULL DEFAULT now(),
  expires_at timestamptz NOT NULL,
  claimed_at timestamptz,
  completed_at timestamptz
);
CREATE INDEX IF NOT EXISTS bhm_research_claim_idx ON public.bhm_research_jobs(state,created_at) WHERE state='queued';
CREATE TABLE IF NOT EXISTS public.bhm_research_nonces (
  host_id text NOT NULL CHECK(host_id IN ('mac-linux','dell-linux')),
  nonce uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY(host_id,nonce)
);
CREATE INDEX IF NOT EXISTS bhm_research_nonce_ts_idx ON public.bhm_research_nonces(created_at);
ALTER TABLE public.bhm_research_devices ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bhm_research_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bhm_research_nonces ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.bhm_research_devices,public.bhm_research_jobs,public.bhm_research_nonces FROM PUBLIC,anon,authenticated;
GRANT SELECT,INSERT,UPDATE,DELETE ON public.bhm_research_devices,public.bhm_research_jobs,public.bhm_research_nonces TO service_role;
COMMENT ON TABLE public.bhm_research_devices IS 'Independent Matrix-only device public keys; no browser PIN/guest/account data';
COMMENT ON TABLE public.bhm_research_jobs IS 'Encrypted Mac-Dell research envelopes only, no plaintext queries';
-- Device public keys are enrolled separately by approved owner action; never commit
-- private keys or runtime identities. No auto-register endpoint exists.
