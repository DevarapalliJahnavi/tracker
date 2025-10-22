from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from db_utils import add_expense, fetch_expense, update_expense, delete_expense
from datetime import datetime

expense_bp = Blueprint('expense', __name__)


@expense_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add_expense.html')

    # POST - validate
    title = request.form.get('title','').strip()
    amount = request.form.get('amount','').strip()
    category = request.form.get('category','').strip()
    date_str = request.form.get('date','').strip()

    errors = []
    if not title:
        errors.append('Title is required')
    try:
        amount_val = float(amount)
        if amount_val <= 0:
            errors.append('Amount must be positive')
    except Exception:
        errors.append('Invalid amount')

    try:
        # normalize date
        dt = datetime.fromisoformat(date_str)
        date_norm = dt.strftime('%Y-%m-%d')
    except Exception:
        errors.append('Invalid date')

    if not category:
        errors.append('Category required')

    if errors:
        for e in errors:
            flash(e, 'danger')
        return redirect(url_for('expense.add'))

    new_id = add_expense(title, amount_val, category, date_norm)
    if new_id:
        flash('Expense added successfully', 'success')
    else:
        flash('Failed to add expense', 'danger')
    return redirect(url_for('dashboard.index'))


@expense_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit(expense_id):
    if request.method == 'GET':
        exp = fetch_expense(expense_id)
        if not exp:
            flash('Expense not found', 'warning')
            return redirect(url_for('dashboard.index'))
        return render_template('edit_expense.html', expense=exp)

    # POST -> update
    title = request.form.get('title','').strip()
    amount = request.form.get('amount','').strip()
    category = request.form.get('category','').strip()
    date_str = request.form.get('date','').strip()

    errors = []
    if not title:
        errors.append('Title is required')
    try:
        amount_val = float(amount)
        if amount_val <= 0:
            errors.append('Amount must be positive')
    except Exception:
        errors.append('Invalid amount')

    try:
        dt = datetime.fromisoformat(date_str)
        date_norm = dt.strftime('%Y-%m-%d')
    except Exception:
        errors.append('Invalid date')

    if errors:
        for e in errors:
            flash(e, 'danger')
        return redirect(url_for('expense.edit', expense_id=expense_id))

    ok = update_expense(expense_id, title, amount_val, category, date_norm)
    if ok:
        flash('Expense updated successfully', 'success')
    else:
        flash('Failed to update expense', 'danger')
    return redirect(url_for('dashboard.index'))


@expense_bp.route('/delete/<int:expense_id>', methods=['GET'])
def delete(expense_id):
    ok = delete_expense(expense_id)
    return jsonify({'success': ok})
