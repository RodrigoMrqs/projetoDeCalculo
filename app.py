from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from models_db import init_db, save_scenario, load_scenarios
from utils import (
    DEFAULT_DATA, 
    calibrate_b_theta, 
    compute_optimum_unconstrained, 
    compute_profit_at_area, 
    generate_profit_plot,
    generate_optimization_plot,
    analyze_with_sympy
)
import io
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
DB_PATH = os.path.join(BASE_DIR, 'projeto.db')

# Inicializa DB se não existir
init_db(DB_PATH)

@app.route('/')
def index():
    """Página inicial com formulário"""
    data = DEFAULT_DATA.copy()
    return render_template('index.html', data=data)

@app.route('/run', methods=['POST'])
def run_model():
    """Processa o modelo e retorna resultados"""
    # Recebe parâmetros do formulário
    A = float(request.form.get('area', 5))
    theta = float(request.form.get('theta', 0.05))

    # Calibra parâmetros a e b
    params = calibrate_b_theta(DEFAULT_DATA, theta)

    # Calcula lucro em A para cada cultura
    profits = {}
    optimization_results = {}
    sympy_analysis = {}
    
    for culture in params:
        a = params[culture]['a']
        b = params[culture]['b']
        
        # Lucro na área A
        profits[culture] = compute_profit_at_area(a, b, A)
        
        # Ponto ótimo (sem restrição)
        optimization_results[culture] = compute_optimum_unconstrained(a, b)
        
        # Análise com SymPy
        sympy_analysis[culture] = analyze_with_sympy(a, b, A)

    # Melhor cultura para área A
    best_culture = max(profits, key=profits.get)
    best_profit = profits[best_culture]
    
    # Melhor cultura considerando ponto ótimo
    best_optimal_culture = max(
        optimization_results,
        key=lambda c: optimization_results[c]['lucro_otimo']
    )

    # Salva cenário no banco
    save_scenario(DB_PATH, {
        'area': A,
        'theta': theta,
        'profits': profits,
        'best': best_culture
    })

    # Gera gráfico de comparação
    img_bytes = generate_profit_plot(profits, A)
    img_path = os.path.join('static', 'last_plot.png')
    os.makedirs('static', exist_ok=True)
    with open(img_path, 'wb') as f:
        f.write(img_bytes.getbuffer())
    
    # Gera gráfico de otimização para a melhor cultura
    opt_img_bytes = generate_optimization_plot(
        params[best_culture]['a'],
        params[best_culture]['b'],
        A
    )
    opt_img_path = os.path.join('static', 'optimization_plot.png')
    with open(opt_img_path, 'wb') as f:
        f.write(opt_img_bytes.getbuffer())

    # Carrega histórico
    scenarios = load_scenarios(DB_PATH)

    return render_template(
        'results.html',
        A=A,
        theta=theta,
        profits=profits,
        best=best_culture,
        best_profit=best_profit,
        optimization_results=optimization_results,
        best_optimal_culture=best_optimal_culture,
        sympy_analysis=sympy_analysis,
        scenarios=scenarios,
        plot_path=img_path,
        opt_plot_path=opt_img_path,
        params=params
    )

@app.route('/scenarios')
def scenarios():
    """API endpoint para cenários"""
    sc = load_scenarios(DB_PATH)
    return {'scenarios': sc}

@app.route('/persona')
def persona():
    """Página da persona"""
    return render_template('persona.html')

if __name__ == '__main__':
    app.run(debug=True)