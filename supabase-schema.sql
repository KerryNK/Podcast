-- Run this in the Supabase SQL Editor for the project used by the Yap Wall.
create extension if not exists pgcrypto;

create table if not exists public.yaps (
  id uuid primary key default gen_random_uuid(),
  author text not null default 'Anonymous' check (char_length(author) between 1 and 40),
  topic text not null check (char_length(topic) between 1 and 48),
  text text not null check (char_length(text) between 1 and 280),
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  flames integer not null default 0 check (flames >= 0),
  mics integer not null default 0 check (mics >= 0),
  created_at timestamptz not null default now()
);

create table if not exists public.replies (
  id uuid primary key default gen_random_uuid(),
  yap_id uuid not null references public.yaps(id) on delete cascade,
  author text not null default 'Listener' check (char_length(author) between 1 and 40),
  text text not null check (char_length(text) between 1 and 280),
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  created_at timestamptz not null default now()
);

create table if not exists public.yap_reactions (
  yap_id uuid not null references public.yaps(id) on delete cascade,
  visitor_id uuid not null,
  reaction text not null check (reaction in ('flames', 'mics')),
  created_at timestamptz not null default now(),
  primary key (yap_id, visitor_id, reaction)
);

create index if not exists yaps_approved_created_at_idx
  on public.yaps (created_at desc) where status = 'approved';
create index if not exists replies_approved_yap_created_at_idx
  on public.replies (yap_id, created_at) where status = 'approved';

alter table public.yaps enable row level security;
alter table public.replies enable row level security;
alter table public.yap_reactions enable row level security;

grant select, insert on public.yaps to anon, authenticated;
grant select, insert on public.replies to anon, authenticated;
revoke all on public.yap_reactions from anon, authenticated;

drop policy if exists "Anyone can read approved yaps" on public.yaps;
create policy "Anyone can read approved yaps" on public.yaps
  for select to anon, authenticated using (status = 'approved');

drop policy if exists "Anyone can submit yaps for moderation" on public.yaps;
create policy "Anyone can submit yaps for moderation" on public.yaps
  for insert to anon, authenticated with check (
    status = 'pending'
    and char_length(trim(author)) between 1 and 40
    and char_length(trim(topic)) between 1 and 48
    and char_length(trim(text)) between 1 and 280
  );

drop policy if exists "Anyone can read approved replies to approved yaps" on public.replies;
create policy "Anyone can read approved replies to approved yaps" on public.replies
  for select to anon, authenticated using (
    status = 'approved'
    and exists (select 1 from public.yaps where yaps.id = replies.yap_id and yaps.status = 'approved')
  );

drop policy if exists "Anyone can submit replies for moderation" on public.replies;
create policy "Anyone can submit replies for moderation" on public.replies
  for insert to anon, authenticated with check (
    status = 'pending'
    and char_length(trim(author)) between 1 and 40
    and char_length(trim(text)) between 1 and 280
    and exists (select 1 from public.yaps where yaps.id = replies.yap_id and yaps.status = 'approved')
  );

create or replace function public.react_to_yap(p_yap_id uuid, p_reaction text, p_visitor_id uuid)
returns table (flames integer, mics integer)
language plpgsql
security definer
set search_path = ''
as $$
declare
  already_reacted boolean;
begin
  if p_reaction not in ('flames', 'mics') then
    raise exception 'Unsupported reaction';
  end if;
  if p_visitor_id is null then
    raise exception 'A visitor ID is required';
  end if;

  if not exists (select 1 from public.yaps where id = p_yap_id and status = 'approved') then
    raise exception 'Yap is unavailable';
  end if;

  delete from public.yap_reactions
    where yap_id = p_yap_id and visitor_id = p_visitor_id and reaction = p_reaction;
  already_reacted := found;

  if already_reacted then
    update public.yaps as y
      set flames = greatest(y.flames - case when p_reaction = 'flames' then 1 else 0 end, 0),
          mics = greatest(y.mics - case when p_reaction = 'mics' then 1 else 0 end, 0)
      where id = p_yap_id;
  else
    insert into public.yap_reactions (yap_id, visitor_id, reaction)
      values (p_yap_id, p_visitor_id, p_reaction);
    update public.yaps as y
      set flames = y.flames + case when p_reaction = 'flames' then 1 else 0 end,
          mics = y.mics + case when p_reaction = 'mics' then 1 else 0 end
      where id = p_yap_id;
  end if;

  return query select y.flames, y.mics from public.yaps as y where y.id = p_yap_id;
end;
$$;

revoke all on function public.react_to_yap(uuid, text, uuid) from public;
grant execute on function public.react_to_yap(uuid, text, uuid) to anon, authenticated;
