-- forMySQL 

use maindb;

CREATE TABLE user(
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_email varchar(100) NOT NULL UNIQUE,
    user_password varchar(150) NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE video(
    video_id INT PRIMARY KEY AUTO_INCREMENT,
    video_name varchar(50) NOT NULL,
    video_url varchar(150) NOT NULL,
    video_owner INT NOT NULL,
    srt_url varchar(150),
    is_converted boolean NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO user(user_email, user_password)
VALUES ('test@email', 'test_password');

INSERT INTO video(video_name, video_url, video_owner, is_converted)
VALUES ('test_video.mp4', 'test_url', 1, false);



-- forPostgreSQL 

-- CREATE TABLE users(
--     user_id SERIAL PRIMARY KEY,
--     user_email varchar(100) NOT NULL UNIQUE,
--     user_password varchar(150) NOT NULL,
--     date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );


-- CREATE TABLE videos(
--     video_id SERIAL PRIMARY KEY,
--     video_name varchar(50) NOT NULL,
--     video_url varchar(150) NOT NULL,
--     video_owner INT NOT NULL,
--     srt_url varchar(150),
--     is_converted boolean NOT NULL,
--     date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- INSERT INTO user(user_email, user_password)
-- VALUES ('test@email', 'test_password');

-- INSERT INTO videos(video_name, video_url, video_owner, is_converted)
-- VALUES ('test_video.mp4', 'test_url', 1, false);