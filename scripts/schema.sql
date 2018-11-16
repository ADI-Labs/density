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
CREATE TABLE oauth_data (
    uni  TEXT NOT NULL,
    code VARCHAR(64) NOT NULL,
    CONSTRAINT oauth_unique_code UNIQUE(code)
);

INSERT INTO buildings (id, name) VALUES
    (115, 'Butler'),
    (124, 'Avery'),
    (99, 'Northwest Corner Building'),
    (2, 'Uris'),
    (97, 'East Asian Library'),
    (153, 'John Jay'),
    (109, 'Lehman Library'),
    (101, 'Lerner');

INSERT INTO routers (id, name, building_id) VALUES
    (104, 'Lerner 3', 101),
    (102, 'Lerner 1', 101),
    (192, 'JJ''s Place', 153),
    (116, 'Butler Library 2', 117),
    (126, 'Architectural and Fine Arts Library 2', 124),
    (121, 'Butler Library 6', 117),
    (98, 'Starr East Asian Library', 97),
    (103, 'Lerner 2', 101),
    (107, 'Roone Arledge Auditorium', 101),
    (120, 'Butler Library 5', 117),
    (111, 'Lehman Library 3', 109),
    (118, 'Butler Library 301', 117),
    (105, 'Lerner 4', 101),
    (100, 'Science and Engineering Library', 99),
    (127, 'Architectural and Fine Arts Library 3', 124),
    (110, 'Lehman Library 2', 109),
    (106, 'Lerner 5', 101),
    (117, 'Butler Library 3', 117),
    (155, 'John Jay Dining Hall', 153),
    (122, 'Butler Library stk', 117),
    (119, 'Butler Library 4', 117),
    (96, 'Uris/Watson Library', 2),
    (125, 'Architectural and Fine Arts Library 1', 124);
