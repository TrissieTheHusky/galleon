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

alter table bot.karma
    owner to defrabot;

create unique index if not exists karma_user_id_uindex
    on bot.karma (user_id);

