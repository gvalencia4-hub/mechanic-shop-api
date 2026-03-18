# My Mechanic Shop API

API documentation and testing project for a mechanic shop system built with Flask.

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone <your-github-repo-url>
cd my-mechanic-shop
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
python app.py
```

---

## 📄 Swagger Documentation

Open in your browser:

```
http://127.0.0.1:5000/api/docs
```

---

## 🧪 Run Tests

```bash
python -m unittest discover tests
```

Expected output:

```
OK
```

---

## ✅ Features Implemented

- Customers API (GET, POST)
- Mechanics API (GET, POST, Top Mechanics)
- Swagger API Documentation
- Unit Testing with unittest

---

## 📌 Notes

- Built using Flask and SQLAlchemy
- Uses Application Factory Pattern
- Designed for learning API development, documentation, and testing
