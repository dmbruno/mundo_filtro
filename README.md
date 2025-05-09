# 🌍 Mundo Filtro

**Mundo Filtro** es una aplicación que se utiliza para llevar registros de los clientes, vehículos y servicios. Almacena la información de los clientes, sus vehículos y los servicios realizados, permitiendo así llevar un control de las visitas y la periodicidad con la que deberían acudir al mantenimiento de cada vehículo.

## 🌐 Tecnologías utilizadas

- 🐍 **Python** con **Flask** como backend
- ⚛️ **React JS** como frontend
- 🗃️ **SQLite** como base de datos
- 🔗 **SQLAlchemy** como ORM

## 🔧 Backend

- Ubicado en la carpeta `/backend`
- Desarrollado con **Python** y **Flask**
- Rutas API REST definidas en `routes/`
- Modelos y migraciones en `models/` y `migrations/`
- Base de datos **SQLite**: `mundo_filtro.db`
- Archivos clave:
  - `app.py`: servidor principal
  - `config.py`: configuración
  - `schema.sql`: script de base de datos
  - `create_tables.py`: script de inicialización
- Soporte para variables de entorno con `.env`

## 🎨 Frontend

- Ubicado en la carpeta `/frontend`
- Desarrollado con **React JS**
- Código principal en `src/`:
  - `components/`: componentes reutilizables
  - `pages/`: vistas de la app
  - `utils/`: funciones y helpers
  - `api.js`: configuración de acceso al backend
- Archivos clave:
  - `App.js`, `App.css`, `index.js`
- Recursos estáticos en `public/` y `assets/`

## 🚀 Características clave

- 📝 Registro y gestión de clientes
- 🚗 Asociación de múltiples vehículos por cliente
- 🛠️ Control de servicios con fechas y tipo de mantenimiento
- ⏰ Seguimiento de mantenimientos para futuras visitas
- 🔎 Búsqueda rápida por cliente o vehículo

## 🛠️ Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/dmbruno/mundo_filtro.git
cd mundo_filtro
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r ../requirements.txt
python app.py
```

### 3. Frontend

```bash
cd ../frontend
npm install
npm start
```

Accede a la app en `http://localhost:3000`.

## 📁 Estructura del proyecto

```
mundo_filtro/
│
├── backend/
│   ├── __pycache__/
│   ├── migrations/
│   ├── models/
│   ├── routes/
│   ├── app.py
│   ├── config.py
│   ├── create_tables.py
│   ├── mundo_filtro.db
│   ├── package.json
│   ├── package-lock.json
│   └── schema.sql
│
├── frontend/
│   ├── build/
│   ├── node_modules/
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── utils/
│   │   ├── api.js
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── App.test.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── reportWebVitals.js
│   │   └── setupTests.js
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
├── requirements.txt
└── README.md
```

## ☁️ Despliegue en producción

Puedes desplegar la app con:

- **Heroku** (Python + Node)
- **Render**
- **Docker** (multi-contenedor con `docker-compose`)
- **VPS** usando Gunicorn + Nginx + servidor Node

## 🙌 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras errores, quieres agregar nuevas funciones o mejorar algo, siéntete libre de hacer un fork del proyecto y enviar un pull request.


## 👨‍💻 Autor

**Diego M Bruno**

📞 Teléfono: +54 387 505-1112  
💼 [LinkedIn](https://www.linkedin.com/in/diego-martin-bruno/)  
📧 Email: dmbruno61@gmail.com

---
## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

¡Gracias por visitar Mundo Filtro!