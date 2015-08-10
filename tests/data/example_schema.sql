create table tasks (
    id          integer primary key autoincrement not null,
    name        text,
    progress    real,
    status      integer default 0,
    d           date,
    ts          timestamp
);
