from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import fetch_expenses, totals_summary, get_settings

import math

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    try:
        expenses = fetch_expenses()
        totals = totals_summary()
        settings = get_settings()
        # Pass data to template
        return render_template('index.html', expenses=expenses, totals=totals, settings=settings)
    except Exception as e:
        print('Error loading dashboard:', e)
        flash('Could not load dashboard', 'danger')
        return render_template('index.html', expenses=[], totals={'total':0,'monthly':0,'highest':0,'used':0,'remaining':settings.get('total_budget',20000)})


@dashboard_bp.route('/stats')
def stats():
    try:
        totals = totals_summary()
        return render_template('stats.html', totals=totals)
    except Exception as e:
        print('Error loading stats:', e)
        flash('Could not load statistics', 'danger')
        return render_template('stats.html', totals={'total':0,'monthly':0,'highest':0,'used':0,'remaining':0})


@dashboard_bp.route('/about')
def about():
    return render_template('about.html')


@dashboard_bp.route('/update_budget', methods=['POST'])
def update_budget_route():
    try:
        new_budget = request.form.get('budget') or request.json.get('budget') if request.is_json else request.form.get('budget')
        if not new_budget:
            flash('Budget value required', 'danger')
            return redirect(url_for('dashboard.index'))
        new_val = float(new_budget)
        from db_utils import update_budget
        ok = update_budget(new_val)
        if ok:
            flash('Budget updated successfully', 'success')
        else:
            flash('Failed to update budget', 'danger')
    except Exception as e:
        print('Error updating budget via form:', e)
        flash('Error updating budget', 'danger')
    return redirect(url_for('dashboard.index'))
