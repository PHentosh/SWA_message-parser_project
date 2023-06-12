CREATE TABLE IF NOT EXISTS main_table (
timest timestamp NOT NULL,
uri varchar(2000),
domain varchar(500),
page_id INT,
page_title varchar(500),
user_text varchar(500),
is_bot BOOLEAN,
user_id INT,
PRIMARY KEY (page_id)
);

CREATE TABLE IF NOT EXISTS domains (
timest INT NOT NULL,
domain varchar(500) NOT NULL,
num INT,
is_bot BOOLEAN,
PRIMARY KEY (domain)
);



-- CREATE TABLE IF NOT EXISTS users (
-- timestamp BIGINT NOT NULL,
-- uri varchar(500),
-- page_id INT,
-- page_title varchar(100),
-- user_text varchar(100),
-- user_id INT NOT NULL,
-- PRIMARY KEY (user_id)
-- );
