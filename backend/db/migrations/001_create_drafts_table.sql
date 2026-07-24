-- ============================================================
-- Migration: Create the `drafts` table
-- Run this in your Supabase SQL Editor (or via psql)
-- ============================================================

create table if not exists public.drafts (
  id              uuid primary key default gen_random_uuid(),
  user_id         uuid not null,
  case_study_id   uuid not null,
  form_data       jsonb not null default '{}',
  updated_at      timestamptz not null default now(),

  -- Only one active draft per user per case study
  unique (user_id, case_study_id)
);

-- Auto-update updated_at on every row change
create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists set_drafts_updated_at on public.drafts;
create trigger set_drafts_updated_at
  before update on public.drafts
  for each row execute procedure public.set_updated_at();

-- RLS: users can only read/write their own drafts
alter table public.drafts enable row level security;

create policy "Users can view their own drafts"
  on public.drafts for select
  using (auth.uid() = user_id);

create policy "Users can insert their own drafts"
  on public.drafts for insert
  with check (auth.uid() = user_id);

create policy "Users can update their own drafts"
  on public.drafts for update
  using (auth.uid() = user_id);

create policy "Users can delete their own drafts"
  on public.drafts for delete
  using (auth.uid() = user_id);

-- Grant access to authenticated users (required since auto-expose is off)
grant select, insert, update, delete on table public.drafts to authenticated;
