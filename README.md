<<<<<<< HEAD
# ASN FARMS

Village farm marketplace built with Django + SQLite (SQL database).

## Features
- **Home** page with animated village background (sun, clouds, birds, coconut trees, huts, walking cow and goat, pecking hen)
- **Navigation bar**: Home, Buyer, Seller, Contact
- **Seller section**: anyone can post an item with image, category, price, location and mobile number
- **Buyer section**: search/filter by item, category, place, max price
- **Privacy flow**: on every card the seller's mobile number is hidden. The visitor opens the card, fills in their own name and mobile, and then ONLY that one seller's number is shown
- **Contact form**: messages saved in the database
- **Admin panel** (`/admin/`): view/hide listings, see who unlocked which number, read contact messages

## Run on your computer

Requires Python 3.10 or newer.

```bash
cd ASN_FARMS

# 1. (recommended) virtual environment
python -m venv venv
# Windows:   venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 2. install packages
pip install -r requirements.txt

# 3. create the database tables (SQLite file db.sqlite3 is created)
python manage.py migrate

# 4. create your admin login
python manage.py createsuperuser

# 5. start the site
python manage.py runserver
```

Open http://127.0.0.1:8000/ and the admin at http://127.0.0.1:8000/admin/

## Where data is stored
SQLite file `db.sqlite3` (tables: market_listing, market_inquiry, market_contactmessage).
Uploaded photos go to the `media/` folder.
To move to MySQL/PostgreSQL later, change `DATABASES` in `asn_farms/settings.py`.

## Project layout
```
ASN_FARMS/
  manage.py
  requirements.txt
  asn_farms/        settings.py, urls.py, wsgi.py
  market/           models.py, forms.py, views.py, urls.py, admin.py, migrations/
  templates/        base.html, _scene.html (animated background), market/*.html
  static/           css/style.css, js/main.js
```

## Background photo (optional)
The animated village scene is drawn in SVG, so it works offline. To use your own
village/animal photo instead, put it at `static/images/village.jpg` and add this
to the end of `static/css/style.css`:

```css
.scene{background:url('/static/images/village.jpg') center/cover no-repeat}
.scene svg{display:none}
```

## Free hosting on PythonAnywhere (recommended)
PythonAnywhere keeps your SQLite database and uploaded photos permanently on the free plan.

1. Create a free "Beginner" account at pythonanywhere.com (your site will be `yourname.pythonanywhere.com`).
2. Upload `ASN_FARMS.zip` (Files tab), then open a **Bash console** and run:
   ```bash
   unzip ASN_FARMS.zip
   cd ASN_FARMS
   mkvirtualenv asn --python=python3.10     # use a Python version PythonAnywhere offers
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```
3. **Web** tab, then **Add a new web app**, choose **Manual configuration**, pick the same Python version.
4. On the Web tab set:
   - **Source code** and **Working directory**: `/home/yourname/ASN_FARMS`
   - **Virtualenv**: `/home/yourname/.virtualenvs/asn`
   - **Static files** (add two rows):
     - URL `/static/` to `/home/yourname/ASN_FARMS/staticfiles`
     - URL `/media/`  to `/home/yourname/ASN_FARMS/media`
5. Click the **WSGI configuration file** link and replace everything with:
   ```python
   import os, sys
   path = '/home/yourname/ASN_FARMS'
   if path not in sys.path:
       sys.path.insert(0, path)
   os.environ['DJANGO_SETTINGS_MODULE'] = 'asn_farms.settings'
   os.environ['DJANGO_DEBUG'] = '0'
   os.environ['DJANGO_SECRET_KEY'] = 'put-a-long-random-string-here'
   os.environ['DJANGO_ALLOWED_HOSTS'] = 'yourname.pythonanywhere.com'
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
6. Press the green **Reload** button and visit `https://yourname.pythonanywhere.com`.

To update later: upload changed files, run `python manage.py migrate` and `collectstatic` if needed, then Reload.

Note: free Render/Railway-style hosts erase uploaded photos and the SQLite file on restart,
so they need an external database and image storage. PythonAnywhere avoids that.

## Notes
- Anyone can post (no login), so check the Admin panel regularly and untick **is_active** to hide bad posts.
- Always keep `DJANGO_DEBUG=0` and a private `DJANGO_SECRET_KEY` on a public site.
=======
# asn_form
>>>>>>> c737a929a098483b7183c27463ac7116a7f214f5
