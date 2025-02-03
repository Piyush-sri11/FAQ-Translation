# FAQ Translation API

This is a **Django REST Framework (DRF)** based API for managing FAQs with **automatic translations** and **caching using Redis**. The API allows users to retrieve FAQs in multiple languages efficiently.

## 🚀 Features
- **Rich Text Support**: FAQs include formatted text (bullets, numbering, etc.).
- **Automatic Translations**: FAQs are automatically translated into multiple languages upon creation.
- **Fast Retrieval with Caching**: Translations are cached using Redis to improve performance.
- **Admin Panel**: Manage FAQs using Django Admin.

---

## 🛠️ Installation Guide

### **1. Clone the Repository**
```sh
 git clone https://github.com/Piyush-sri11/FAQ-Translation.git
```

### **2. Set Up a Virtual Environment**
```sh
 python -m venv env
 source env/bin/activate  # On Windows use: env\Scripts\activate
```

### **3. Install Dependencies**
```sh
 pip install -r requirements.txt
```

### **4. Run Migrations**
```sh
 python manage.py migrate
```

### **5. Create a Superuser** (For Django Admin Access)
```sh
 python manage.py createsuperuser
```

### **6. Start Redis Server**
Ensure Redis is installed and running before starting the Django server.

#### **On Ubuntu/Debian**
```sh
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server.service
sudo systemctl start redis-server.service
```

#### **On macOS**
```sh
brew install redis
brew services start redis
```

#### **On Windows**
1. Download Redis from the [official website](https://redis.io/download).
2. Extract the zip file and run `redis-server.exe`.

#### **On WSL**
```sh
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

Ensure Redis is running by executing:
```sh
redis-cli ping
```
You should see `PONG` as the response.

### **7. Run the Django Server**
```sh
 python manage.py runserver
```

---

## 📌 API Usage

### **1. Get All FAQs (Default: English)**
```http
GET /api/faqs/
```
**Response:**
```json
[
  {
    "id": 1,
    "question": "What is your return policy?",
    "answer": "You can return within 30 days.",
  }
]
```

### **2. Get FAQs in a Specific Language**
```http
GET /api/faqs/?lang=fr
```
**Response:**
```json
[
  {
    "id": 1,
    "question": "Quelle est votre politique de retour ?",
    "answer": "Vous pouvez retourner dans les 30 jours.",
  }
]
```

### **3. Add a New FAQ (Admin Only)**
```http
POST /admin/faq/faq/add/
```
Admins can add new FAQs through the Django Admin Panel.

### **4. Retrieve Translated FAQ (Cached)**
Translations are cached in Redis for faster retrieval.

---

## Testing
### **Running Tests**

#### **1. Pytest**
We use `pytest` for running tests. To run the tests, execute:
```sh
pytest --disable-warnings
```

#### **2. Flake8**
We use `flake8` for linting the code. To check for linting errors, execute:
```sh
flake8
```

### **Defined Pytests**

- **Test for FAQ Retrieval**
- **Test for Adding a New FAQ**
- **Test for Cached Translation Retrieval**


## 🛠️ Contribution Guidelines
We welcome contributions! To contribute:
1. **Fork the repository**.
2. **Create a new branch** for your feature/fix.
3. **Commit your changes** and push to your fork.
4. **Submit a pull request**.

### **Coding Guidelines**
- Follow **PEP8** for Python code.
- Use **meaningful commit messages**.
- Ensure **tests pass** before submitting a PR.

### **Reporting Issues**
If you find a bug or have a feature request, please [open an issue](https://github.com/Piyush-sri11/FAQ-Translation/issues).

---

## ⚡ Future Enhancements
- Containerizing the application using Dockerfile and docker-compose.yml
- Deploying on AWS or Heroku
---

## 📝 License
This project is licensed under the **MIT License**.

---



