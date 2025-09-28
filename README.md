# 🗳️ Online Poll System Backend

A Django REST Framework (DRF) powered backend API for creating polls, casting votes, and retrieving results.  
The project also integrates **Swagger/OpenAPI documentation** for easy exploration and testing of endpoints.

---

## 🚀 Features

- Create, update, and delete polls
- Add multiple choices to a poll
- Cast votes on polls
- View poll results in real-time
- Interactive API documentation with **Swagger UI**
- PostgreSQL database (hosted on Render)
- Deployed with **Render Free Tier**

---

## 📂 Project Structure

online-poll-backend/
│── polls_api/ # Main Django project folder
│ ├── settings.py # Django settings (Render & Postgres config)
│ ├── urls.py # Root URLs (API + Swagger docs + homepage)
│ └── views.py # Homepage view
│
│── polls/ # App for poll models, views, serializers, and endpoints
│── requirements.txt # Dependencies
│── Procfile # Entry point for Render deployment
│── README.md # Project documentation

---
