CREATE TABLE course(
	id INT,
	title VARCHAR(150) UNIQUE,
    link VARCHAR(150) UNIQUE,
    coupon_code VARCHAR(50),
    date_found DATETIME NOT NULL,
	PRIMARY KEY (id)
);