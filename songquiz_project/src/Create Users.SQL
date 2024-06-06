CREATE TABLE IF NOT EXISTS users( username char(20) NOT NULL,
    password char(20) NOT NULL,
    CONSTRAINT user_pk PRIMARY KEY (username));

copy  users(username,password)
            from '/PATH/TO/PROJECT/songquiz_project/tmp/users.csv' -- Change path here!
            delimiter ','
            CSV HEADER;
