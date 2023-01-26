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
    video_is_private boolean NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO user(user_email, user_password)
VALUES ('test_email', 'test_password');

INSERT INTO video(video_name, video_url, video_owner, video_is_private)
VALUES ('test_video', 'test_url', 1, true);