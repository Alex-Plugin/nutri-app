# 🥗 Nutri-app — Nutrition Tracking Django Project

Nutri-app is a web application that helps users track daily calories and macronutrients (proteins, fats, carbohydrates).  
The system allows users to create and categorize products, log meals, calculate daily nutritional intake, and estimate personal calorie needs using established formulas.

---

## 🌐 Live Demo
The project is deployed and available online:

### 👉 Live App
https://nutri-app-5wjm.onrender.com

## 👤 Test User
You can explore the application using a test account:

login: user  
password: user12345

## 🚀 Features

### 🔐 Authentication & User Management
- User registration and login/logout.
- Extended custom user model (`Customer`) with:
  - age  
  - height  
  - weight  
  - gender  
  - activity level  
- Additional validation for age, weight, and height.
- Marking the currently logged-in user with a **(Me)** badge in the user list.

### 🍽 Nutrition Tracking
- Add and manage food **categories**, **products**, and **meals**.
- Track calories, proteins, fats, and carbs based on product quantity (in grams).
- Automatic total nutrition calculation for each meal.

### 📊 Personal Calorie Calculations
- BMR calculated with the **Harris-Benedict Equation**.
- Daily calorie needs (TDEE) based on selected activity level.

### 🔎 Smart Search & Lists
All list views include:
- Search forms
- Pagination (5 items per page)
- Clean, table-based display

Meal search is implemented with date selection using **Flatpickr**.

### 👥 Meal Sharing
- Users may share meals with other users.
- List view displays personal meals first, then shared ones.

### 🎨 UI & Frontend
- Built with **Bootstrap 5** and **Crispy Forms**.
- Based on Django template theme **Pixel**.
- Responsive layout with reusable template components.

---

## 📚 Technologies Used

### Backend
- **Python 3**
- **Django 4.1**

### Database
- **SQLite** (development)
- **PostgreSQL** (optional production configuration)

### Frontend
- **Bootstrap 5**
- **Crispy Forms (crispy-bootstrap5)**
- **Flatpickr** (date picker)

### Development Tools
- **flake8**, pep8-naming, flake8-quotes  
- Django Debug Toolbar

---

## 🧩 Data Models

### **Customer**
Extended `AbstractUser` with:
- age, height, weight
- gender
- activity_level  
Methods:
- `get_bmr()`
- `get_tdee()`

### **Category**
Product categories (e.g. Fruits, Vegetables).

### **Product**
Food products with nutritional values per 100 g:
- calories  
- proteins  
- fats  
- carbs  

### **Meal**
Logged meal with:
- product
- quantity in grams
- date
- optional sharing with other users  
Computed fields:
- total_calories
- total_proteins
- total_fats
- total_carbs

---

## 📂 Project Structure

`````
nutri-app/
├── manage.py
├── README.md
├── requirements.txt
├── db.sqlite3
├── nutri_app/ # Django project configuration
├── nutrition/ # Main application
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── urls.py
│ ├── tests/
├── templates/ # Jinja templates
│ ├── nutrition/
│ ├── registration/
├── static/ # CSS / JS / Images
`````


---

## ▶️ Installation & Run

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd nutri-app
`````

### 2. Create & activate virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Apply migrations
```
python manage.py migrate
```

### 5. Create a superuser (optional)
```
python manage.py createsuperuser
```

### 6. Run the server
```
python manage.py runserver
```

## 🧪 Tests
Unit tests are located in:
```
nutrition/tests/
```
To run tests:
```
python manage.py test
```

## 📸 Model Diagram
A visual schema of all models is available at:
```
0_models_diagram.png
```

## 📝 Optional Features Included

Meal sharing system

Flatpickr calendar for date filtering

Custom validation for user physical data

Pagination on all list pages

## 📄 License
This project is part of educational work and is distributed for learning purposes.








