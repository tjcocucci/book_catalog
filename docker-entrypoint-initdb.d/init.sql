CREATE DATABASE IF NOT EXISTS books;

CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'AdminPass123!';

GRANT ALL PRIVILEGES ON books.* TO 'admin'@'%';
GRANT ALL PRIVILEGES ON test_books.* TO 'admin'@'%';

FLUSH PRIVILEGES;
