CREATE TABLE websites(
    web_id      INT(5) NOT NULL,
    webname VARCHAR(20) NOT NULL,
    url     VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE images(
    img_id          INT(20) NOT NULL,
    url         VARCHAR(2083) NOT NULL,
    page_url    VARCHAR(2083) NOT NULL,
    PRIMARY KEY(img_id)
);

CREATE TABLE imgtags(
    img_id      INT(20) NOT NULL,
    tag_id      INT(10) NOT NULL,
    weight      INT(10),
    FOREIGN KEY(img_id) REFERENCES images(img_id)
);
