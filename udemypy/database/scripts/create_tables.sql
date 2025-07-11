CREATE TABLE course(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title VARCHAR(150) UNIQUE,
    link VARCHAR(150) UNIQUE,
    coupon_code VARCHAR(50),
    date_found DATETIME,
    discount INTEGER,
    discount_time_left VARCHAR(25),
    students VARCHAR(25),
    rating VARCHAR(25),
    lang VARCHAR(25),
    badge VARCHAR(25)
);

CREATE TABLE social_media(
	id INTEGER PRIMARY KEY,
    name VARCHAR(150) UNIQUE,
    udemypy_username VARCHAR(25),
    udemypy_profile_link VARCHAR(25)
);

CREATE TABLE course_social_media(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	course_id INTEGER,
    social_media_id INTEGER,
    date_time_shared DATETIME NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course(id),
    FOREIGN KEY (social_media_id) REFERENCES social_media(id)
);