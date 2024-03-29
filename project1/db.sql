--
-- blog post table
--
CREATE TABLE blog (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  description_enc TEXT,
  date_created TEXT NOT NULL,
  last_modified TEXT,
  tags TEXT,
  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

--
-- comments table
--
CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  comments TEXT NOT NULL,
  date_created TEXT NOT NULL,
  user_id INTEGER,
  blog_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (blog_id) REFERENCES blog(id)
);

--
-- users tbale
--
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL
);
