/*
CREATE TABLE IF NOT EXISTS usuarios (
    id intenger PRIMARY KEY, 
    nombre text NOT NULL,
    dni intenger NOT NULL
    /*
    id intenger PRIMARY KEY,
    apellido text NOT NULL,
    nombre text NOT NULL,
    dni intenger NOT NULL,
    email boolean NOT NULL,
    num_telefono intenger
    
);
*/

CREATE TABLE aulas (
    id_aulas INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    cant_max_usuarios VARCHAR NOT NULL
);


CREATE UNIQUE INDEX aulas_idx ON aulas( nombre );


CREATE TABLE usuarios (
    id_usuarios INTEGER PRIMARY KEY,
    apellido VARCHAR NOT NULL,
    nombre VARCHAR NOT NULL,
    dni INTEGER NOT NULL,
    email VARCHAR,
    num_telefono INTEGER
);


CREATE UNIQUE INDEX usuarios_idx ON usuarios( dni );

CREATE TABLE relacion_usuarios_aulas (
    id_aulas INTEGER NOT NULL,
    id_usuarios INTEGER NOT NULL,
    PRIMARY KEY (id_aulas, id_usuarios),
    FOREIGN KEY (id_aulas) REFERENCES aulas(id_aulas)
    FOREIGN KEY (id_usuarios) REFERENCES usuarios(id_usuarios)
);


/*ALTER TABLE relacion_usuarios_aulas ADD CONSTRAINT aulas_relacion_usuarios_aulas_fk
FOREIGN KEY (id_aulas)
REFERENCES aulas (id_aulas)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE relacion_usuarios_aulas ADD CONSTRAINT usuarios_relacion_usuarios_aulas_fk
FOREIGN KEY (id_usuarios)
REFERENCES usuarios (id_usuarios)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
/**/
