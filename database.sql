-- Guilds settings table script --

create table if not exists bot.guilds
(
    guild_id      bigint                       not null
        constraint guilds_pk
            primary key,
    prefix        text,
    admin_roles   bigint[] default '{}'::bigint[],
    mod_roles     bigint[] default '{}'::bigint[],
    trusted_roles bigint[] default '{}'::bigint[],
    _timezone     text     default 'UTC'::text not null,
    language      text
);

comment on table bot.guilds is 'Settings of every guild';

create unique index if not exists guilds_guild_id_uindex
    on bot.guilds (guild_id);

alter table bot.guilds
    owner to defrabot;

-- Logging table --

create table if not exists bot.logging_channels
(
    guild_id       bigint                          not null
        constraint logging_channels_pk
            primary key,
    misc           bigint[] default '{}'::bigint[] not null,
    messages       bigint[] default '{}'::bigint[] not null,
    join_leave     bigint[] default '{}'::bigint[] not null,
    mod_actions    bigint[] default '{}'::bigint[] not null,
    config_logs    bigint[] default '{}'::bigint[] not null,
    server_changes bigint[] default '{}'::bigint[] not null
);

comment on table bot.logging_channels is 'guild_id - represents guild
misc - some commands usage logs
messages - deleted and edited messages, maybe spam violations
join_leave - basically new members
mod_actions - mutes, bans, kicks and etc.
config_logs - someone changed bot config
server_changes - new channels, roles, added/removed roles and other things like that (actually might be useless cuz audit logs)';

create unique index if not exists logging_channels_guild_id_uindex
    on bot.logging_channels (guild_id);

alter table bot.blacklist
    owner to defrabot;

-- Blacklist table --

create table if not exists bot.blacklist
(
    user_id bigint not null
);

create unique index if not exists blacklist_user_id_uindex
    on bot.blacklist (user_id);

alter table bot.blacklist
    owner to defrabot;

-- Infractions table script --

create table if not exists bot.infractions
(
    inf_id       bigserial                                              not null
        constraint infractions_pk
            primary key,
    guild_id     bigint                                                 not null,
    moderator_id bigint                                                 not null,
    target_id    bigint                                                 not null,
    reason       text      default 'no reason,'::text                   not null,
    inf_type     text                                                   not null,
    added_at     timestamp default (now())::timestamp without time zone not null,
    expires_at   timestamp default (now())::timestamp without time zone not null
);

alter table bot.infractions
    owner to defrabot;

create unique index infractions_inf_id_uindex
    on bot.infractions (inf_id);

-- Stats table script --

create table if not exists bot.stats
(
    user_id       bigint not null,
    messages_sent bigint default 0
);

comment on table bot.stats is 'Some stats';

alter table bot.stats
    owner to defrabot;

create unique index if not exists stats_user_id_uindex
    on bot.stats (user_id);

-- Karma counter table --

create table if not exists bot.karma
(
    user_id     bigint                                                 not null
        constraint karma_pk
            primary key,
    karma       bigint    default 0,
    modified_at timestamp default (now())::timestamp without time zone not null
);

comment on table bot.karma is 'users karma data';

create unique index if not exists karma_user_id_uindex
    on bot.karma (user_id);

alter table bot.karma
    owner to defrabot;

-- Todos table --

create table if not exists bot.todos
(
    user_id   bigint not null,
    content   text   not null,
    timestamp timestamp default (now())::timestamp without time zone
);

alter table bot.todos
    owner to defrabot;
