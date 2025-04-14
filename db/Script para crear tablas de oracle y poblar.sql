-- PARA BORRAR TABLAS 
-- DROP TABLE JUEGO;
-- DROP TABLE CATEGORIA;
-- DROP TABLA USUARIO;


-- CREAR TABLA CATEGORIA

CREATE TABLE Categoria (
    id NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    titulo VARCHAR2(100) NOT NULL,
    lema VARCHAR2(255),
    descripcion VARCHAR2(500),
    imagen VARCHAR2(255)
);

-- CREAR TABLA JUEGO

CREATE TABLE Juego (
    id NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(500),
    precio NUMBER(10) NOT NULL,
    categoria_id NUMBER,  -- Relación con Categoria
    plataformas VARCHAR2(255),
    imagen VARCHAR2(255),

    -- Definir la relación con Categoria
    CONSTRAINT fk_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES Categoria(id) ON DELETE CASCADE
);


-- CREAR TABLA USUARIO
CREATE TABLE Usuario (
    id NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    nombre_completo VARCHAR2(200) NOT NULL,
    nombre_usuario VARCHAR2(50) UNIQUE NOT NULL,
    correo_electronico VARCHAR2(100) UNIQUE NOT NULL,
    contrasena VARCHAR2(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion_despacho VARCHAR2(255),
    rol VARCHAR2(20) CHECK (rol IN ('administrador', 'vendedor', 'cliente', 'invitado'))
);



-- Insertar categorias en la tabla CATEGORIA

INSERT INTO CATEGORIA (ID, NOMBRE, TITULO, LEMA, DESCRIPCION, IMAGEN) 
VALUES (1, 'Carreras', 'Carreras', '🏎️ Carreras: La velocidad lo es todo.', 
        'Compite en emocionantes circuitos, domina curvas cerradas y deja atrás a tus rivales en intensas carreras llenas de adrenalina.',
        '/static/img/carreras.jpg');

INSERT INTO CATEGORIA (ID, NOMBRE, TITULO, LEMA, DESCRIPCION, IMAGEN) 
VALUES (2, 'Cozy', 'Cozy', '☕ Cozy: Relájate y disfruta.', 
        'Juegos tranquilos con ambientaciones acogedoras, mecánicas relajantes y un ritmo pausado para desconectar del estrés.',
        '/static/img/cozy.jpg');

INSERT INTO CATEGORIA (ID, NOMBRE, TITULO, LEMA, DESCRIPCION, IMAGEN) 
VALUES (3, 'mundoabierto', 'Mundo Abierto', '🌍 Mundo Abierto: Explora sin límites.',
        'Aventúrate en vastos mundos llenos de secretos, desafíos y personajes inolvidables. La historia la escribes tú.',
        '/static/img/mundo-abierto.jpg');

INSERT INTO CATEGORIA (ID, NOMBRE, TITULO, LEMA, DESCRIPCION, IMAGEN) 
VALUES (4, 'Shooters', 'Shooters', '🎯 Shooters: Acción sin descanso.',
        'Enfréntate a enemigos en intensos tiroteos, ya sea en combates tácticos, arenas frenéticas o guerras épicas.',
        '/static/img/shooters.jpg');

INSERT INTO CATEGORIA (ID, NOMBRE, TITULO, LEMA, DESCRIPCION, IMAGEN) 
VALUES (5, 'Terror', 'Terror', '👻 Terror: Sobrevive a la pesadilla.',
        'Sumérgete en historias escalofriantes, evade horrores indescriptibles y enfrenta el miedo en cada sombra.',
        '/static/img/terror.jpg');




-- Insertar juegos en la tabla JUEGO

INSERT INTO Juego (nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES ('Crash Team Racing Nitro-Fueled', 
        'Revive la emoción de las carreras arcade con Crash y sus amigos. Derrapa a toda velocidad, usa ítems locos y domina los circuitos llenos de obstáculos en este vibrante remake del clásico de PlayStation.', 
        20000, 1, 'PS4, Xbox One, Nintendo Switch, PC', '/static/img/crashteamracing.jpg');

INSERT INTO Juego (nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES ('Mario Kart 8 Deluxe', 
        'Compite en pistas alocadas, usa ítems estratégicos y disfruta de la mejor experiencia multijugador de carreras con Mario y sus amigos.', 
        49990, 1, 'Nintendo Switch', '/static/img/mariokart8deluxe.jpg');


INSERT INTO Juego (id, nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES (3, 'Stardew Valley', 
        'En Stardew Valley, heredas una granja descuidada de tu abuelo y decides dejar atrás la vida en la ciudad para restaurarla. Con mecánicas de cultivo, crianza de animales, pesca, minería y relaciones con los habitantes del pueblo. Su pixel art encantador y la música nostálgica lo convierten en un clásico del género cozy.',
        14990, 2, 'PS4, Xbox One, Nintendo Switch, PC', '/static/img/stardewvalley.jpg');

INSERT INTO Juego (nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES ('Spiritfarer', 
        'En Spiritfarer, juegas como Stella, una guía de almas encargada de llevar a los espíritus al más allá. A bordo de tu barco, debes cuidar a estos entrañables personajes, completar sus últimas peticiones y ayudarlos a encontrar paz antes de despedirse. El juego combina mecánicas de gestión y exploración con una narrativa emotiva y visuales pintados a mano. Es una experiencia conmovedora sobre la vida, la muerte y la importancia de las relaciones.', 
        29990, 2, 'PS4, Xbox One, Nintendo Switch, PC', '/static/img/spiritfarer.jpg');

INSERT INTO Juego (nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES ('Cyberpunk 2077', 
        'Sumérgete en Night City, una metrópolis futurista donde las decisiones cambian el curso de la historia. Personaliza a tu personaje, mejora tus implantes cibernéticos y descubre una narrativa profunda llena de acción y conspiraciones.', 
        59990, 3, 'PS4, Xbox One, PC', '/static/img/cyberpunk2077.jpg');

INSERT INTO Juego (nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES ('The Legend of Zelda: Tears of the Kingdom', 
        'La épica secuela de Breath of the Wild amplía Hyrule con nuevas mecánicas, poderes y misterios en un mundo lleno de posibilidades. Descubre secretos ocultos en el cielo y la tierra mientras forjas tu propia aventura.', 
        69990, 3, 'Nintendo Switch', '/static/img/zeldatotk.jpg');

INSERT INTO Juego (nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES ('DOOM Eternal', 
        'Acción frenética y sin descanso. Enfréntate a hordas de demonios con un arsenal brutal en este shooter que combina velocidad, estrategia y una banda sonora que te mantendrá en constante adrenalina.', 
        39990, 4, 'PS4, Xbox One, PC', '/static/img/doometernal.jpg');

INSERT INTO Juego (nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES ('Splatoon 2', 
        'Un shooter único donde la tinta es tu mejor arma. Compite en equipos para cubrir el escenario con tu color, personaliza a tu Inkling y disfruta de batallas dinámicas llenas de estilo y diversión.', 
        49990, 4, 'Nintendo Switch', '/static/img/splatoon2.jpg');

INSERT INTO Juego (nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES ('Alan Wake 2', 
        'Un thriller psicológico oscuro e inquietante. Sigue a Alan en su lucha contra fuerzas sobrenaturales mientras la realidad y la ficción se entrelazan en una historia aterradora y envolvente.', 
        59999, 5, 'PS5, Xbox Series X/S, PC', '/static/img/alanwake2.jpg');

INSERT INTO Juego (nombre, descripcion, precio, categoria_id, plataformas, imagen)
VALUES ('Resident Evil 4 Remake', 
        'Una reimaginación del clásico de terror y acción. Acompaña a Leon S. Kennedy en su misión de rescate mientras enfrenta horrores inimaginables en un pueblo lleno de misterio y peligros.', 
        59999, 5, 'PS4, PS5, Xbox Series X/S, PC', '/static/img/residentevil4remake.jpg');


-- VER TABLAS

SELECT * FROM CATEGORIA;
SELECT * FROM JUEGO;
SELECT * FROM USUARIO;

