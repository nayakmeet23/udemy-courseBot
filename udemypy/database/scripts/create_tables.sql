CREATE TABLE IF NOT EXISTS course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    coupon_code TEXT,
    date_found TEXT NOT NULL,
    current_price TEXT NOT NULL DEFAULT '0',
    previous_price TEXT,
    rating REAL NOT NULL DEFAULT 4.5,
    category TEXT,
    image_url TEXT NOT NULL,
    students TEXT,
    language TEXT,
    badge TEXT,
    discount_time_left TEXT,
    source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS social_media(
	id INTEGER PRIMARY KEY,
    name VARCHAR(150) UNIQUE,
    udemypy_username VARCHAR(25),
    udemypy_profile_link VARCHAR(25)
);

CREATE TABLE IF NOT EXISTS course_social_media(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	course_id INTEGER,
    social_media_id INTEGER,
    date_time_shared DATETIME NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course(id),
    FOREIGN KEY (social_media_id) REFERENCES social_media(id)
);