CREATE TABLE feedback_data(
    id                  INTEGER NOT NULL,
    building_id         INTEGER NOT NULL,
    percentage_change   INTEGER NOT NULL,
    raw_count           INTEGER NOT NULL,
    PRIMARY KEY(id)
);

"""
to migrate to the db, run command

$psql postgresql://adicu:voyageurcrackingtritiumcolanderstoreyleaflet@adicu.com:5432/density < scripts/migrations.sql
"""