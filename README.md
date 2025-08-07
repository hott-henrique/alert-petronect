# 📦 Petronect

Petronect is a modular Python application for extracting, processing, and matching public bidding opportunities from the **Petronect** platform. It automates the collection and evaluation of bid data, supports email notifications, and uses serverless functions and background workers for scalable, efficient processing.

---

## 🚀 Features

- **📊 Data Extraction & Processing**: Collects and processes bidding data, attachments, and user alerts.
- **🗂 Modular Architecture**: Separates models, data, and persistence logic for maintainability.
- **📦 Serverless Execution**: Stateless functions handle tasks like downloading, processing, and matching bids.
- **📧 Email Notifications**: Notifies users of relevant bid matches.
- **🐳 Docker-Ready**: Includes `Dockerfile` and `docker-compose` for easy deployment.
- **🌀 Asynchronous Processing**: Uses Celery to queue and process tasks in the background.
- **🔄 Database Versioning**: Alembic used for managing schema migrations.
