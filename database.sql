create table bot.guilds
(
    guild_id      bigint not null,
    prefix        text     default null,
    admin_roles   bigint[] default '{}',
    mod_roles     bigint[] default '{}',
    trusted_roles bigint[] default '{}',
    mod_logs      bigint[] default '{}'
);

comment on table bot.guilds is 'Settings of every guild';

create unique index guilds_guild_id_uindex
    on bot.guilds (guild_id);

alter table bot.guilds
    add constraint guilds_pk
        primary key (guild_id);



create table bot.infractions
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