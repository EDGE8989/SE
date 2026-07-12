# Component Diagram

```mermaid
graph TD
    subgraph "Frontend Layer (Browser)"
        UI[HTML5 / CSS3 / Vanilla JS]
        Charts[Chart.js]
        Icons[Font Awesome]
    end

    subgraph "Application Layer (Flask)"
        App[Flask App Factory]
        Routes[Blueprints (Routing)]
        Auth[Flask-Login]
        Templates[Jinja2 Templates]
        Uploads[File Upload Handler]
    end

    subgraph "Data Layer"
        ORM[SQLAlchemy ORM]
        SQLite[(SQLite Database)]
    end

    UI -->|HTTP GET/POST| Routes
    Charts -->|JSON Data| Routes
    Routes --> Templates
    Routes --> Auth
    Routes --> Uploads
    Routes --> ORM
    Auth --> ORM
    ORM --> SQLite
```
