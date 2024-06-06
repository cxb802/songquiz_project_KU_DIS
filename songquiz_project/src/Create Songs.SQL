CREATE TABLE IF NOT EXISTS Songs (
    Album char(100),
    Artist char(10000),
    Lyrics char(1000000),
    Title char(100),
    id int,
    word_search_column char(1000000),
    CONSTRAINT song_pk PRIMARY KEY (id)
);

COPY Songs(Album, Artist, Lyrics, Title, id,word_search_column)
FROM '/PATH/TO/PROJECT/songquiz_project/tmp/filtered_song.csv' -- Change path here!
DELIMITER ','
CSV HEADER;