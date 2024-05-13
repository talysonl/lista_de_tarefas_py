código mysql usado:

CREATE DATABASE IF NOT EXISTS StarkTaskManager;
USE StarkTaskManager;

CREATE TABLE IF NOT EXISTS Tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE,
    status ENUM('A Fazer', 'Em Andamento', 'Concluído') NOT NULL
);

credenciais usadas: 

host="localhost",
user="root",
password="Co010910BR7!",
database="StarkTaskManager"



////////// no arquivo .rar enviado, contém um executável dessa aplicação. 