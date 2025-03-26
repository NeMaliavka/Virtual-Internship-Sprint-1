-- Добавление поля status в таблицу pereval_added
ALTER TABLE pereval_added
ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'new';

-- Добавление ограничения на поле status
ALTER TABLE pereval_added
ADD CONSTRAINT status_check CHECK (status IN ('new', 'pending', 'accepted', 'rejected'));

-- Создание таблицы Users
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы Coords
CREATE TABLE Coords (
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    height INTEGER NOT NULL
);

-- Обновление таблицы pereval_added для использования coord_id
ALTER TABLE pereval_added
ADD COLUMN coord_id INTEGER REFERENCES Coords(id);

-- Добавление полей для уровня сложности
ALTER TABLE pereval_added
ADD COLUMN level_spring TEXT,
ADD COLUMN level_summer TEXT,
ADD COLUMN level_autumn TEXT,
ADD COLUMN level_winter TEXT;

-- Создание таблицы pereval_images
CREATE TABLE pereval_images (
    id SERIAL PRIMARY KEY,
    pereval_id INTEGER REFERENCES pereval_added(id),
    image_name VARCHAR(255) NOT NULL
);