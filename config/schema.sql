DROP TABLE density_data CASCADE;
DROP TABLE oauth_data CASCADE;
DROP TABLE routers CASCADE;
DROP TABLE buildings CASCADE;

CREATE TABLE buildings (
    id      INTEGER NOT NULL,
    name    TEXT NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT building_unique_name UNIQUE(name)
);

CREATE TABLE routers (
    id              INTEGER NOT NULL,
    name            TEXT NOT NULL,
    building_id     INTEGER NOT NULL REFERENCES buildings,
    PRIMARY KEY(id),
    CONSTRAINT room_unique_name UNIQUE(name)
);

CREATE TABLE density_data (
    dump_time       TIMESTAMP,
    group_id        INTEGER NOT NULL REFERENCES routers,
    client_count    INTEGER NOT NULL,
    PRIMARY KEY(dump_time, group_id)
);

CREATE INDEX ON density_data (group_id, dump_time);
CREATE INDEX ON density_data (parent_id);
CREATE TABLE oauth_data (
    uni  TEXT NOT NULL,
    code VARCHAR(64) NOT NULL,
    CONSTRAINT oauth_unique_code UNIQUE(code)
);

INSERT INTO buildings (id, name) VALUES
    (103, 'Butler'),
    (146, 'Avery'),
    (15,  'Northwest Corner Building'),
    (2,   'Uris'),
    (62,  'East Asian Library'),
    (75,  'John Jay'),
    (79,  'Lehman Library'),
    (84,  'Lerner');

INSERT INTO routers (id, name, building_id) VALUES
    (152, 'Lerner 3', 84),
    (150, 'Lerner 1', 84),
    (155, 'JJ''s Place', 75),
    (130, 'Butler Library 2', 103),
    (148, 'Architectural and Fine Arts Library 2', 146),
    (134, 'Butler Library 6', 103),
    (144, 'Starr East Asian Library', 62),
    (151, 'Lerner 2', 84),
    (85,  'Roone Arledge Auditorium', 84),
    (133, 'Butler Library 5', 103),
    (140, 'Lehman Library 3', 79),
    (171, 'Butler Library 301', 103),
    (153, 'Lerner 4', 84),
    (145, 'Science and Engineering Library', 15),
    (149, 'Architectural and Fine Arts Library 3', 146),
    (139, 'Lehman Library 2', 79),
    (154, 'Lerner 5', 84),
    (131, 'Butler Library 3', 103),
    (125, 'John Jay Dining Hall', 75),
    (138, 'Butler Library stk', 103),
    (132, 'Butler Library 4', 103),
    (23,  'Uris/Watson Library',  2),
    (147, 'Architectural and Fine Arts Library 1', 146);
