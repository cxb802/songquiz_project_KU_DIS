CREATE TABLE IF NOT EXISTS favorites (
    id INT,
    username VARCHAR(20),
    Artist VARCHAR(10000),
    Title VARCHAR(100),
    PRIMARY KEY (id, username)
);