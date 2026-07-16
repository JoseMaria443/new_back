-- 1. CATÁLOGOS BASE (Diccionarios de datos)
-- Tablas planas para nutrir las listas desplegables del sistema.

CREATE TABLE AREA (
    idArea UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(150) UNIQUE NOT NULL -- Nombre del área (ej. "Ingeniería de Software", "Biblioteca")
);

CREATE TABLE CARGO (
    idCargo UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) UNIQUE NOT NULL -- Nombre del cargo funcional (ej. "Jefe de Departamento", "Secretaria")
);

CREATE TABLE TIPO_COMUNICADO (
    idTipoComunicado UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) UNIQUE NOT NULL -- Catalogación (ej. "Oficio", "Circular", "Informativo")
);

CREATE TABLE MEDIO_RECEPCION (
    idMedioRecepcion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) UNIQUE NOT NULL -- Medio de llegada (ej. "Físico", "Correo", "WhatsApp")
);

CREATE TABLE ROL_DESTINATARIO (
    idRolDestinatario UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    descripcionRol VARCHAR(100) UNIQUE NOT NULL -- Rol de quien recibe el comunicado (ej. "Principal", "Con Copia")
);

CREATE TABLE ROL_RESPONSABLE (
    idRolResponsable UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    descripcionRol VARCHAR(100) UNIQUE NOT NULL -- Rol operativo en la tarea (ej. "Líder", "Apoyo Técnico")
);

CREATE TABLE ESTADO_TAREA (
    idEstadoTarea UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(50) UNIQUE NOT NULL -- asignada, cancelada, retrasada, entregada, revisada, rechazada, terminada
);

-- 2. GESTIÓN DE PERSONAL Y AUDITORÍA
-- Separación de los datos personales (Empleado) de los cargos organizacionales.

CREATE TABLE EMPLEADO (
    idEmpleado UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) NOT NULL, -- Nombre completo del trabajador
    email VARCHAR(150) UNIQUE NOT NULL, -- Correo institucional
    idArea UUID NOT NULL, -- A qué área pertenece físicamente/administrativamente
    activo BOOLEAN DEFAULT TRUE, -- Estatus lógico del empleado (activo/licencia)
    fechaRegistro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Cuándo se dio de alta
    CONSTRAINT fkEmpleadoArea FOREIGN KEY (idArea) REFERENCES AREA(idArea) ON DELETE RESTRICT
);

-- Tabla Pivote: Un empleado puede tener múltiples cargos simultáneamente.
CREATE TABLE EMPLEADO_CARGO (
    idEmpleado UUID NOT NULL, -- ID del trabajador
    idCargo UUID NOT NULL, -- ID del cargo asignado
    fechaRegistro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Cuándo se le otorgó el cargo
    PRIMARY KEY (idEmpleado, idCargo),
    CONSTRAINT fkEcEmpleado FOREIGN KEY (idEmpleado) REFERENCES EMPLEADO(idEmpleado) ON DELETE CASCADE,
    CONSTRAINT fkEcCargo FOREIGN KEY (idCargo) REFERENCES CARGO(idCargo) ON DELETE CASCADE
);

CREATE TABLE HISTORIAL_ESTATUS (
    idHistorial UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idEmpleadoAfectado UUID NOT NULL, -- A quién se le aplicó la licencia/activación
    idEmpleadoModifica UUID NOT NULL, -- Qué usuario del sistema ejecutó el cambio
    accion VARCHAR(50) NOT NULL CHECK (accion IN ('DESACTIVACION', 'REACTIVACION')), -- Tipo de movimiento
    fechaRegistro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Momento exacto del cambio
    -- Nota: Se eliminó el atributo "motivo" por instrucción.
    CONSTRAINT fkHistorialAfectado FOREIGN KEY (idEmpleadoAfectado) REFERENCES EMPLEADO(idEmpleado) ON DELETE CASCADE,
    CONSTRAINT fkHistorialModifica FOREIGN KEY (idEmpleadoModifica) REFERENCES EMPLEADO(idEmpleado) ON DELETE RESTRICT
);

-- 3. NÚCLEO DOCUMENTAL (COMUNICADOS)
-- Matriz principal de todo documento que entra, sale o circula en la universidad.

CREATE TABLE COMUNICADO (
    idComunicado UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    folioDoi VARCHAR(100) UNIQUE NOT NULL, -- Identificador único global en el repositorio
    numComunicado VARCHAR(50) NOT NULL, -- Numeración institucional (ej. "DIR-2026-001/A")
    tema VARCHAR(200) NOT NULL, -- Asunto general del comunicado
    
    fechaEmision TIMESTAMP WITH TIME ZONE NOT NULL, -- Cuándo se firmó originalmente el documento
    fechaRecepcion TIMESTAMP WITH TIME ZONE NOT NULL, -- Cuándo llegó físicamente/digitalmente
    fechaRegistro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Cuándo se tecleó en BD
    
    idEmisor UUID NOT NULL, -- Empleado que redacta/envía el documento
    idTipoComunicado UUID NOT NULL, -- Referencia al catálogo (Circular, Oficio, etc.)
    idMedioRecepcion UUID NOT NULL, -- Cómo nos llegó este comunicado
    idEmpleadoRegistro UUID NOT NULL, -- Quién fue la persona que capturó los datos en pantalla
    
    CONSTRAINT fkComunicadoEmisor FOREIGN KEY (idEmisor) REFERENCES EMPLEADO(idEmpleado) ON DELETE RESTRICT,
    CONSTRAINT fkComunicadoTipo FOREIGN KEY (idTipoComunicado) REFERENCES TIPO_COMUNICADO(idTipoComunicado) ON DELETE RESTRICT,
    CONSTRAINT fkComunicadoMedio FOREIGN KEY (idMedioRecepcion) REFERENCES MEDIO_RECEPCION(idMedioRecepcion) ON DELETE RESTRICT,
    CONSTRAINT fkComunicadoRegistro FOREIGN KEY (idEmpleadoRegistro) REFERENCES EMPLEADO(idEmpleado) ON DELETE RESTRICT
);

-- Tabla pivote: Permite mandar 1 comunicado a muchos destinatarios, especificando su rol.
CREATE TABLE COMUNICADO_DESTINATARIO (
    idComunicado UUID NOT NULL, -- Documento en cuestión
    idDestinatario UUID NOT NULL, -- Empleado al que va dirigido
    idRolDestinatario UUID NOT NULL, -- Si va como principal, con copia, etc.
    fechaRegistro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Cuándo se hizo la vinculación
    PRIMARY KEY (idComunicado, idDestinatario),
    CONSTRAINT fkCdComunicado FOREIGN KEY (idComunicado) REFERENCES COMUNICADO(idComunicado) ON DELETE CASCADE,
    CONSTRAINT fkCdDestinatario FOREIGN KEY (idDestinatario) REFERENCES EMPLEADO(idEmpleado) ON DELETE CASCADE,
    CONSTRAINT fkCdRol FOREIGN KEY (idRolDestinatario) REFERENCES ROL_DESTINATARIO(idRolDestinatario) ON DELETE RESTRICT
);

CREATE TABLE COMUNICADO_ARCHIVO (
    idArchivo UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idComunicado UUID NOT NULL, -- A qué comunicado pertenece el adjunto
    urlArchivo VARCHAR(500) NOT NULL, -- Ruta en S3 / Servidor
    nombreOriginal VARCHAR(255) NOT NULL, -- Nombre original del archivo (ej. "acta.pdf")
    fechaRegistro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Cuándo se adjuntó
    CONSTRAINT fkCaComunicado FOREIGN KEY (idComunicado) REFERENCES COMUNICADO(idComunicado) ON DELETE CASCADE
);

-- 4. FLUJO OPERATIVO (TAREAS Y RESPONSABLES)
-- Cualquier comunicado puede derivar (o no) en una Tarea.

CREATE TABLE TAREA (
    idTarea UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idComunicado UUID NOT NULL, -- Documento que detonó la obligación
    idEstadoTarea UUID NOT NULL, -- Estatus dinámico (asignada, cancelada, etc.)
    
    resumenActividad TEXT NOT NULL, -- Explicación breve (Dashboard)
    descripcion TEXT NOT NULL, -- Instrucciones profundas de lo que hay que hacer
    fechaEntrega TIMESTAMP WITH TIME ZONE NOT NULL, -- Cuándo debe estar lista la evidencia
    fechaRegistro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Cuándo se creó la tarea
    
    CONSTRAINT fkTareaComunicado FOREIGN KEY (idComunicado) REFERENCES COMUNICADO(idComunicado) ON DELETE CASCADE,
    CONSTRAINT fkTareaEstado FOREIGN KEY (idEstadoTarea) REFERENCES ESTADO_TAREA(idEstadoTarea) ON DELETE RESTRICT
);

-- Tabla Pivote: Quiénes están asignados a la tarea y qué rol juegan (Responsable/Colaborador).
CREATE TABLE TAREA_RESPONSABLE (
    idTarea UUID NOT NULL, -- Tarea a ejecutar
    idResponsable UUID NOT NULL, -- Empleado designado
    idRolResponsable UUID NOT NULL, -- Referencia al catálogo de roles de tarea
    fechaRegistro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Cuándo se le asignó
    PRIMARY KEY (idTarea, idResponsable),
    CONSTRAINT fkTrTarea FOREIGN KEY (idTarea) REFERENCES TAREA(idTarea) ON DELETE CASCADE,
    CONSTRAINT fkTrResponsable FOREIGN KEY (idResponsable) REFERENCES EMPLEADO(idEmpleado) ON DELETE CASCADE,
    CONSTRAINT fkTrRol FOREIGN KEY (idRolResponsable) REFERENCES ROL_RESPONSABLE(idRolResponsable) ON DELETE RESTRICT
);

-- 5. CUMPLIMIENTO (EVIDENCIAS)
-- Archivos comprobatorios y su vinculación a las tareas.

-- La tabla maestra de archivos subidos como prueba de trabajo.
CREATE TABLE ARCHIVO_EVIDENCIA (
    idArchivoEvidencia UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doi VARCHAR(100) UNIQUE NOT NULL, -- Identificador del archivo en el repositorio
    descripcion TEXT NOT NULL, -- Anotación específica de lo que contiene esta evidencia
    urlArchivo VARCHAR(500) NOT NULL, -- Ruta física en la nube
    nombreOriginal VARCHAR(255) NOT NULL, -- Ej: "foto_junta_final.jpg"
    idElaborador UUID NOT NULL, -- El empleado que generó/subió el archivo
    fechaRegistro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Sello de tiempo de subida
    CONSTRAINT fkAeElaborador FOREIGN KEY (idElaborador) REFERENCES EMPLEADO(idEmpleado) ON DELETE RESTRICT
);

-- Tabla Puente Pura: Conecta el archivo de evidencia con la tarea específica.
-- No requiere fechaRegistro ni ID propio, ya que es estrictamente asociativa.
CREATE TABLE TAREA_EVIDENCIA (
    idTarea UUID NOT NULL,
    idArchivoEvidencia UUID NOT NULL,
    PRIMARY KEY (idTarea, idArchivoEvidencia),
    CONSTRAINT fkTeTarea FOREIGN KEY (idTarea) REFERENCES TAREA(idTarea) ON DELETE CASCADE,
    CONSTRAINT fkTeArchivo FOREIGN KEY (idArchivoEvidencia) REFERENCES ARCHIVO_EVIDENCIA(idArchivoEvidencia) ON DELETE CASCADE
);

-- ÍNDICES DE RENDIMIENTO (Optimización de Consultas)
CREATE INDEX idxComunicadoDoi ON COMUNICADO(folioDoi);
CREATE INDEX idxComunicadoNum ON COMUNICADO(numComunicado);
CREATE INDEX idxEmpleadoArea ON EMPLEADO(idArea);
CREATE INDEX idxDestinatariosEmpleado ON COMUNICADO_DESTINATARIO(idDestinatario);
CREATE INDEX idxResponsablesEmpleado ON TAREA_RESPONSABLE(idResponsable);
CREATE INDEX idxTareaComunicado ON TAREA(idComunicado);