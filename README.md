# IN16 Study Manager 🎓

A full-featured Django class management app for IN16 Software Engineering students.  
Login · Notes · Units · Groups · Class List · Announcements · Reminders · Dark Mode

---

## Features

- 🔐 Register / Login with student profile (reg number, gender)
- 📚 Units with note & group counts
- 📝 Per-unit notes with full-detail view
- 👥 Study groups with member listings
- 🎓 Full class list with search & gender filter
- 📣 Announcements board
- ⏰ Personal study reminders
- 🌙 Dark mode toggle
- 📱 Fully responsive (Bootstrap 5)
- ⚙️ Django Admin panel

---

## 🚀 Deploy to Railway (Step-by-Step)

### 1. Push to GitHub

```bash
cd BISWA_CLASS_MANAGER
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/biswa-class-manager.git
git push -u origin main
```

### 2. Create Railway project

1. Go to [railway.app](https://railway.app) and sign in
2. Click **New Project → Deploy from GitHub repo**
3. Select your repo

### 3. Set environment variables in Railway dashboard

Go to your service → **Variables** tab → add these:

| Variable | Value |
|---|---|
| `SECRET_KEY` | `any-long-random-string-here` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*` |
| `DATABASE_URL` | `postgresql://postgres.sgqypmhvoljfdbzpldka:Nabiswa1james@aws-1-eu-west-1.pooler.supabase.com:6543/postgres` |
| `CSRF_TRUSTED_ORIGINS` | `https://YOUR-APP-NAME.up.railway.app` |

> **Tip:** Once deployed, copy your Railway URL and use it as `CSRF_TRUSTED_ORIGINS`

### 4. Seed the database (run once after first deploy)

In Railway dashboard → your service → **Shell** tab:

```bash
python manage.py seed
```

Or from your local machine with the Supabase DATABASE_URL:

```bash
export DATABASE_URL="postgresql://postgres.sgqypmhvoljfdbzpldka:Nabiswa1james@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"
python manage.py seed
```

### 5. Access your app

- App: `https://YOUR-APP.up.railway.app`
- Admin: `https://YOUR-APP.up.railway.app/admin/` → `admin / admin123`
- Student login: `kevinkiptoo / pass1234`

---

## 🚀 Deploy to Render (Alternative)

1. Create **New Web Service** on [render.com](https://render.com)
2. Connect your GitHub repo
3. Set:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn IN16_Study_Manager.wsgi --bind 0.0.0.0:$PORT`
4. Add the same environment variables as above
5. After deploy, open **Shell** and run `python manage.py seed`

---

## 💻 Run Locally

```bash
# 1. Clone and enter project
git clone https://github.com/YOUR_USERNAME/biswa-class-manager.git
cd biswa-class-manager

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up local .env (uses SQLite by default if no DATABASE_URL)
cp .env.example .env

# 5. Run migrations
python manage.py migrate

# 6. Seed sample data
python manage.py seed

# 7. Start server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 🗂️ Project Structure

```
BISWA_CLASS_MANAGER/
├── manage.py
├── requirements.txt          ← Django, gunicorn, psycopg2, whitenoise
├── Procfile                  ← Railway/Heroku process definition
├── railway.toml              ← Railway build/deploy config
├── runtime.txt               ← Python 3.11.9
├── seed_data.py              ← Quick seed script
├── .env                      ← Local environment variables (DO NOT COMMIT)
├── .env.example              ← Template – safe to commit
├── .gitignore
├── IN16_Study_Manager/
│   ├── settings.py           ← Production-ready settings
│   ├── urls.py
│   └── wsgi.py
└── notes_app/
    ├── models.py             ← Unit, Student, Note, Group, Announcement, Reminder
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    ├── management/
    │   └── commands/
    │       └── seed.py       ← python manage.py seed [--clear]
    └── templates/
        └── notes_app/
            ├── base.html
            ├── login.html
            ├── register.html
            ├── home.html
            ├── units.html
            ├── notes.html
            ├── note_detail.html
            ├── groups.html
            ├── students.html
            ├── announcements.html
            └── reminders.html
```

---

## Default Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Student | `kevinkiptoo` | `pass1234` |
| Student | `lynettechepkemoi` | `pass1234` |

> Change admin password immediately after first login in production!

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5 |
| Frontend | Bootstrap 5.3 + Bootstrap Icons |
| Fonts | Sora + JetBrains Mono |
| Database | PostgreSQL (Supabase) / SQLite (local) |
| Static files | WhiteNoise |
| Server | Gunicorn |
| Auth | Django built-in |
