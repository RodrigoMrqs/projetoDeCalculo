from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from models_db import init_db, save_scenario, load_scenarios
from utils import (DEFAULT_DATA, calibrate_b_theta, compute_optimum_unconstrained, compute_profit_at_area, generate_profit_plot)
import io
import os

app = Flask(__name__)
DB_PATH = 'projeto.db'

# Inicializa DB se não existir
init_db(DB_PATH)

@app.route('/')
def index():
    # mostra formulário com dados default
    data = DEFAULT_DATA.copy()
    return render_template('index.html', data=data)

@app.route('/run', methods=['POST'])
def run_model():
    # Recebe A (area total) e theta do form
    A = float(request.form.get('area', 5))
    theta = float(request.form.get('theta', 0.05))

    # Calibra b_i e calcula lucros em A
    params = calibrate_b_theta(DEFAULT_DATA, theta)

    # calcula L_i(A) e encontra melhor cultura
    profits = {c: compute_profit_at_area(params[c]['a'], params[c]['b'], A)
               for c in params}

    best_culture = max(profits, key=profits.get)
    best_profit = profits[best_culture]

    # salva cenário no DB
    save_scenario(DB_PATH, {'area': A, 'theta': theta, 'profits': profits, 'best': best_culture})

    # gera figura em memória
    img_bytes = generate_profit_plot(profits, A)

    # Salva imagem temporariamente
    img_path = os.path.join('static', 'last_plot.png')
    os.makedirs('static', exist_ok=True)
    with open(img_path, 'wb') as f:
        f.write(img_bytes.getbuffer())

    scenarios = load_scenarios(DB_PATH)

    return render_template('results.html', A=A, theta=theta, profits=profits,
                           best=best_culture, best_profit=best_profit,
                           scenarios=scenarios, plot_path=img_path)

@app.route('/scenarios')
def scenarios():
    sc = load_scenarios(DB_PATH)
    return {'scenarios': sc}

if __name__ == '__main__':
    app.run(debug=True)
