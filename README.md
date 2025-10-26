# 🌍 Country & Currency API

A Django REST Framework project  built by **Kabiru Kolawole** that fetches, stores, and manages country and currency data from an external API.  
It provides endpoints to refresh data, retrieve countries, add new entries, and handle validation errors gracefully.

---

## 🚀 Features

- Fetch countries and currencies from an external API (`restcountries.com`).
- Store data in a database.
- Retrieve all or specific countries.
- Create or delete country records.
- Automatic validation for required fields.
- Proper error handling for invalid or missing data.

---

## ⚙️ Tech Stack
- **Python 3.13+**
- **Django 5+**
- **Django REST Framework**
- **django-environ** (for `.env` configuration)
- **Requests** (for external API calls)
- **PyMySQL** (for MySQL integration)

---
## Endpoints
- **POST** /countries/refresh → Fetch all countries and exchange rates, then cache them in the database
- **GET** /countries → Get all countries from the DB (support filters and sorting) - ?region=Africa | ?currency=NGN | ?sort=gdp_desc
- **GET** /countries/:name → Get one country by name
- **DELETE** /countries/:name → Delete a country record
- **GET** /status → Show total countries and last refresh timestamp
- **GET** /countries/image → serve summary image

---
## 🧩 Project Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/cozy1712/country_exchange_api.git
cd country-currency-api

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# or
source venv/bin/activate   # On macOS/Linux
```
3️⃣ Install Dependencies
```bash

pip install -r requirements.txt

```
4️⃣ Create a .env File
```bash
At the project root, create a .env file:

DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=mysql://user:password@localhost:3306/your_db_name
COUNTRIES_URL=https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
EXCHANGE_URL=https://open.er-api.com/v6/latest
```
5️⃣ Apply Migrations
```bash

python manage.py makemigrations
python manage.py migrate

```
6️⃣ Run the Server
```bash
python manage.py runserver

```
---

## 🔗 API Endpoints

### **Base URL**
Server runs on:

👉 http://127.0.0.1:8000/
```

---


🧾 Example Requests

✅ Refresh Countries Data

POST /api/refresh

```bash
Response (200 OK):

{
  "message": "Refresh successful",
  "total_countries": 250
}
```
---

✅ Get All Countries
GET /api/countries

```bash
Response (200 OK):

[
  {
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 25767448125.2,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2025-10-22T18:00:00Z"
  }
]

```
---