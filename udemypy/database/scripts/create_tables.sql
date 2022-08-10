CREATE TABLE course(
	id INT,
	title VARCHAR(150) UNIQUE,
    link VARCHAR(150) UNIQUE,
    coupon_code VARCHAR(50),
    date_found DATETIME,
    discount INT,
    discount_time_left VARCHAR(25),
    students VARCHAR(25),
    rating VARCHAR(25),
    lang VARCHAR(25),
    badge VARCHAR(25),
	PRIMARY KEY (id)
);

CREATE TABLE social_media(
	id INT,
    name VARCHAR(150) UNIQUE,
    udemypy_username VARCHAR(25),
    udemypy_profile_link VARCHAR(25),
	PRIMARY KEY (id)
);

CREATE TABLE course_social_media(
	id INT,
	course_id INT,
    social_media_id INT,
    date_time_shared DATETIME NOT NULL,
	PRIMARY KEY (id),
    FOREIGN KEY (course_id) REFERENCES course(id),
    FOREIGN KEY (social_media_id) REFERENCES social_media(id)
);