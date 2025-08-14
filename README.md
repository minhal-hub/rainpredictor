# RainPredictor

A Django web app that lets users **sign up / log in**, submit a **location + date**, and get a **rain probability** using the open-source **Open‑Meteo** API.  
All prediction requests are stored per‑user in PostgreSQL. A simple JSON API is also provided with cURL examples.

---

## Features

- Django **Class-Based Views** (no FBVs)
- **Signup / Login / Logout** using Django auth
- **PostgreSQL** storage; DB credentials pulled from `config.json`
- **Open‑Meteo** geocoding + forecast (no API key required)
- Track **PredictionHistory** per user
- JSON API: `POST /api/predict/`
- Clean repo with `requirements.txt`, `README.md`, `migrations/`

---

## Quickstart

### 1) Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Create PostgreSQL DB
```sql
-- in psql or your GUI
CREATE DATABASE rainpredictor;
```

### 4) Configure `config.json`
Create a file `config.json` in the project root:
```json
{
  "SECRET_KEY": "change-me-please-very-secret-key",
  "DEBUG": true,
  "ALLOWED_HOSTS": ["*"],
  "DATABASE": {
  "ENGINE": "django.db.backends.postgresql",
  "NAME": "rainpredictor",
  "USER": "rainuser",
  "PASSWORD": "rainpass",
  "HOST": "127.0.0.1",
  "PORT": "5432"
}
}
```

### 5) Run migrations + create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6) Run the dev server
```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. Sign up or log in, then use the **Predict** page.

---

## API

### Endpoint
```
POST /api/predict/
Content-Type: application/json

{ "location": "Lahore", "date": "2025-08-15" }
```

### Sample JSON Response
```json
{
  "location": "Lahore",
  "country": "Pakistan",
  "date": "2025-08-15",
  "rain_chance_percent": 42.0
}
```

> Note: The API requires authentication (session-based). For simplicity, the endpoint is CSRF-exempt.

### cURL flow (login then call API)

1) Get login page to receive cookies (including csrftoken):

```bash
curl -i -c cookies.txt http://127.0.0.1:8000/accounts/login/
```

2) Extract the CSRF token (optional here since `/api/predict/` is CSRF-exempt; still needed to post login form):

```bash
CSRFTOKEN=$(grep csrftoken cookies.txt | tail -n 1 | awk '{print $7}')
echo $CSRFTOKEN
```

3) Log in (replace with your actual username/password):

```bash
curl -i -b cookies.txt -c cookies.txt \
  -H "Referer: http://127.0.0.1:8000/accounts/login/" \
  -d "username=<your_username>&password=<your_password>&csrfmiddlewaretoken=$CSRFTOKEN" \
  -X POST http://127.0.0.1:8000/accounts/login/
```

4) Call the API:

```bash
curl -s -b cookies.txt -H "Content-Type: application/json" \
  -d '{"location":"Lahore","date":"2025-08-15"}' \
  -X POST http://127.0.0.1:8000/api/predict/ | jq .
```

---

## Project Structure

```
rainpredictor/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── config.json               # (create locally; not committed)
├── rainpredictor/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       └── __init__.py
├── prediction/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       └── 0001_initial.py
└── templates/
    ├── base.html
    ├── registration/
    │   └── login.html
    ├── accounts/
    │   └── signup.html
    └── prediction/
        ├── index.html
        └── history.html
```

---

## Notes

- **Open‑Meteo** is used for free geocoding + forecast; no API key required.
- Keep real secrets out of git. `config.json` is ignored by `.gitignore`.
- All views are **class-based** as requested.
