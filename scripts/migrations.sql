DROP TABLE feedback_data CASCADE;

CREATE TABLE feedback_data(
    group_id         	INTEGER NOT NULL,
    raw_count           INTEGER NOT NULL,
    percentage_change   INTEGER NOT NULL
);
