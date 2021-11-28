CREATE TABLE tasks (
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    school TEXT NOT NULL,
    gps TEXT NOT NULL,
    gps_loc_name TEXT NOT NULL,
    alias TEXT NOT NULL UNIQUE,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE INDEX tasks_id_IDX ON tasks (id);
CREATE INDEX tasks_username_IDX ON tasks (username);