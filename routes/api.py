from flask import Blueprint, jsonify, request
from db_utils import fetch_expenses, fetch_expense, totals_summary, get_settings, update_budget
from collections import defaultdict
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/expenses', methods=['GET'])
def api_expenses():
    try:
        rows = fetch_expenses()
        return jsonify({'success': True, 'data': rows})
    except Exception as e:
        print('Error fetching expenses for API:', e)
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/stats/category', methods=['GET'])
def api_stats_category():
    try:
        rows = fetch_expenses()
        agg = defaultdict(float)
        for r in rows:
            agg[r['category']] += float(r['amount'])
        data = [{'category': k, 'total': v} for k, v in agg.items()]
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        print('Error building category stats:', e)
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/stats/monthly', methods=['GET'])
def api_stats_monthly():
    try:
        rows = fetch_expenses()
        agg = defaultdict(float)
        for r in rows:
            # assume date stored as YYYY-MM-DD
            dt = r['date']
            key = dt[:7] if dt else 'unknown'
            agg[key] += float(r['amount'])
        # sort by month
        items = sorted(agg.items())
        data = [{'month': k, 'total': v} for k, v in items]
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        print('Error building monthly stats:', e)
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/budget', methods=['GET'])
def api_budget():
    try:
        totals = totals_summary()
        return jsonify({'success': True, 'data': {'budget': totals.get('budget'), 'used': totals.get('used'), 'remaining': totals.get('remaining')}})
    except Exception as e:
        print('Error fetching budget:', e)
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/update_budget', methods=['POST'])
def api_update_budget():
    try:
        payload = request.get_json() or {}
        new_budget = float(payload.get('budget', 0))
        if new_budget <= 0:
            return jsonify({'success': False, 'error': 'Budget must be positive'}), 400
        ok = update_budget(new_budget)
        return jsonify({'success': ok})
    except Exception as e:
        print('Error updating budget:', e)
        return jsonify({'success': False, 'error': str(e)}), 500
