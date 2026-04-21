create table if not exists public.listings (
    id bigint generated always as identity primary key,
    title text not null,
    district text not null,
    rooms integer not null check (rooms > 0),
    price bigint not null check (price > 0),
    created_at timestamptz not null default now()
);

alter table public.listings add column if not exists title text;
alter table public.listings add column if not exists district text;
alter table public.listings add column if not exists rooms integer;
alter table public.listings add column if not exists price bigint;
alter table public.listings add column if not exists created_at timestamptz default now();
alter table public.listings add column if not exists owner_id uuid;

update public.listings set district = coalesce(district, 'Не указан') where district is null;
update public.listings set rooms = coalesce(rooms, 1) where rooms is null;
update public.listings set price = coalesce(price, 1) where price is null;

alter table public.listings alter column title set not null;
alter table public.listings alter column district set not null;
alter table public.listings alter column rooms set not null;
alter table public.listings alter column price set not null;

create index if not exists listings_owner_id_idx on public.listings(owner_id);

alter table public.listings enable row level security;

drop policy if exists "Public read listings" on public.listings;
create policy "Public read listings"
on public.listings
for select
to anon, authenticated
using (true);

drop policy if exists "Authenticated insert listings" on public.listings;
create policy "Authenticated insert listings"
on public.listings
for insert
to authenticated
with check (owner_id = auth.uid());

drop policy if exists "Owner update listings" on public.listings;
create policy "Owner update listings"
on public.listings
for update
to authenticated
using (owner_id = auth.uid())
with check (owner_id = auth.uid());

drop policy if exists "Owner delete listings" on public.listings;
create policy "Owner delete listings"
on public.listings
for delete
to authenticated
using (owner_id = auth.uid());

create table if not exists public.favorites (
    id bigint generated always as identity primary key,
    user_id uuid not null references auth.users(id) on delete cascade,
    listing_id bigint not null references public.listings(id) on delete cascade,
    created_at timestamptz not null default now(),
    unique(user_id, listing_id)
);

create index if not exists favorites_user_id_idx on public.favorites(user_id);
create index if not exists favorites_listing_id_idx on public.favorites(listing_id);

alter table public.favorites enable row level security;

drop policy if exists "Users select own favorites" on public.favorites;
create policy "Users select own favorites"
on public.favorites
for select
to authenticated
using (user_id = auth.uid());

create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    email text,
    username text,
    created_at timestamptz not null default now()
);

alter table public.profiles add column if not exists email text;
alter table public.profiles add column if not exists username text;
alter table public.profiles add column if not exists created_at timestamptz default now();
alter table public.profiles add column if not exists is_blocked boolean not null default false;

create index if not exists profiles_username_idx on public.profiles(username);
create index if not exists profiles_email_idx on public.profiles(email);

alter table public.profiles enable row level security;

drop policy if exists "Public read profiles" on public.profiles;
create policy "Public read profiles"
on public.profiles
for select
to authenticated, anon
using (true);

drop policy if exists "Users upsert own profile" on public.profiles;
create policy "Users upsert own profile"
on public.profiles
for insert
to authenticated
with check (id = auth.uid());

drop policy if exists "Users update own profile" on public.profiles;
create policy "Users update own profile"
on public.profiles
for update
to authenticated
using (id = auth.uid())
with check (id = auth.uid());

drop policy if exists "Users insert own favorites" on public.favorites;
create policy "Users insert own favorites"
on public.favorites
for insert
to authenticated
with check (user_id = auth.uid());

drop policy if exists "Users delete own favorites" on public.favorites;
create policy "Users delete own favorites"
on public.favorites
for delete
to authenticated
using (user_id = auth.uid());

create table if not exists public.chats (
    id bigint generated always as identity primary key,
    created_by uuid not null references auth.users(id) on delete cascade,
    created_at timestamptz not null default now()
);

create table if not exists public.chat_members (
    id bigint generated always as identity primary key,
    chat_id bigint not null references public.chats(id) on delete cascade,
    user_id uuid not null references auth.users(id) on delete cascade,
    created_at timestamptz not null default now(),
    unique(chat_id, user_id)
);

create table if not exists public.messages (
    id bigint generated always as identity primary key,
    chat_id bigint not null references public.chats(id) on delete cascade,
    sender_id uuid not null references auth.users(id) on delete cascade,
    body text not null,
    created_at timestamptz not null default now()
);

create index if not exists chat_members_chat_id_idx on public.chat_members(chat_id);
create index if not exists chat_members_user_id_idx on public.chat_members(user_id);
create index if not exists messages_chat_id_idx on public.messages(chat_id);
create index if not exists messages_sender_id_idx on public.messages(sender_id);

alter table public.chats enable row level security;
alter table public.chat_members enable row level security;
alter table public.messages enable row level security;

do $$
declare r record;
begin
    for r in (
        select policyname
        from pg_policies
        where schemaname = 'public' and tablename = 'chats'
    )
    loop
        execute format('drop policy if exists %I on public.chats', r.policyname);
    end loop;
end $$;

do $$
declare r record;
begin
    for r in (
        select policyname
        from pg_policies
        where schemaname = 'public' and tablename = 'chat_members'
    )
    loop
        execute format('drop policy if exists %I on public.chat_members', r.policyname);
    end loop;
end $$;

do $$
declare r record;
begin
    for r in (
        select policyname
        from pg_policies
        where schemaname = 'public' and tablename = 'messages'
    )
    loop
        execute format('drop policy if exists %I on public.messages', r.policyname);
    end loop;
end $$;

drop policy if exists "Members can view chats" on public.chats;
create policy "Members can view chats"
on public.chats
for select
to authenticated
using (
    created_by = auth.uid()
    or
    exists (
        select 1 from public.chat_members cm
        where cm.chat_id = chats.id and cm.user_id = auth.uid()
    )
);

drop policy if exists "Users create chats" on public.chats;
create policy "Users create chats"
on public.chats
for insert
to public
with check (true);

drop policy if exists "Members view chat_members" on public.chat_members;
create policy "Members view chat_members"
on public.chat_members
for select
to authenticated
using (user_id = auth.uid());

drop policy if exists "Users insert own chat_members" on public.chat_members;
create policy "Users insert own chat_members"
on public.chat_members
for insert
to public
with check (true);

drop policy if exists "Members view messages" on public.messages;
create policy "Members view messages"
on public.messages
for select
to authenticated
using (
    exists (
        select 1 from public.chat_members cm
        where cm.chat_id = messages.chat_id and cm.user_id = auth.uid()
    )
);

drop policy if exists "Members send messages" on public.messages;
create policy "Members send messages"
on public.messages
for insert
to authenticated
with check (
    sender_id = auth.uid()
    and exists (
        select 1 from public.chat_members cm
        where cm.chat_id = messages.chat_id and cm.user_id = auth.uid()
    )
);

-- Listing cover image (public URL in this column)
alter table public.listings add column if not exists image_url text;

-- Map markers (WGS84). Optional: both null or both set from the app.
alter table public.listings add column if not exists latitude double precision;
alter table public.listings add column if not exists longitude double precision;
alter table public.listings add column if not exists is_premium boolean not null default false;

create index if not exists listings_premium_id_idx
on public.listings(is_premium, id desc);

-- Storage: public bucket for listing photos (path: {user_id}/{filename})
insert into storage.buckets (id, name, public)
values ('listing-images', 'listing-images', true)
on conflict (id) do update set public = excluded.public;

drop policy if exists "listing images public read" on storage.objects;
create policy "listing images public read"
on storage.objects
for select
to public
using (bucket_id = 'listing-images');

drop policy if exists "listing images owner insert" on storage.objects;
create policy "listing images owner insert"
on storage.objects
for insert
to authenticated
with check (
    bucket_id = 'listing-images'
    -- Path must be {auth.uid()}/... (same rule the app uses)
    and name like auth.uid()::text || '/%'
);

drop policy if exists "listing images owner update" on storage.objects;
create policy "listing images owner update"
on storage.objects
for update
to authenticated
using (
    bucket_id = 'listing-images'
    and name like auth.uid()::text || '/%'
)
with check (
    bucket_id = 'listing-images'
    and name like auth.uid()::text || '/%'
);

drop policy if exists "listing images owner delete" on storage.objects;
create policy "listing images owner delete"
on storage.objects
for delete
to authenticated
using (
    bucket_id = 'listing-images'
    and name like auth.uid()::text || '/%'
);
