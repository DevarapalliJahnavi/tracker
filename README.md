Expense Tracker - Frontend

This folder contains a complete Bootstrap 5 frontend for an Expense Tracker web app designed to integrate with a Flask backend.

Structure:
- templates/ - HTML pages (index, add_expense, edit_expense, stats, about)
- static/css/style.css - main styles (glassmorphism, gradients, responsive)
- static/js/main.js - theme, AOS, Rellax, CountUp, interactions
- static/js/charts.js - Chart.js charts for stats page
- static/sounds/click.mp3 - click sound for UI interactions
- static/img/waves.svg - decorative parallax layer

How to use with Flask:
- Serve `templates/` as Flask templates and `static/` as static folder (default for Flask)
- Replace placeholder data in templates/charts with server-side templating (Jinja)

Notes:
- External libraries are loaded via CDN (Bootstrap, AOS, Rellax, CountUp, Chart.js)
- Theme preference stored in localStorage under `exp_theme`. Sound preference stored under `exp_sound`.

# tracker
# tracker
