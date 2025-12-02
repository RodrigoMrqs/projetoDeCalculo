import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import sympy as sp

# optional libs
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

try:
    from pycaret.regression import setup as pyc_setup, compare_models
    PYC_AVAILABLE = True
except Exception:
    PYC_AVAILABLE = False

# Dados extraídos do artigo
DEFAULT_DATA = {
    'Milho': {'P': 70262.27},
    'Feijao': {'P': 40593.61},
    'Macaxeira': {'P': 77468.64},
    'Batata-doce': {'P': 75692.15}
}

def calibrate_b_theta(data_dict, theta=0.05):
    """
    Calibra os parâmetros a e b do modelo L(x) = ax - bx²
    
    Parâmetros:
    - a = P (lucro por hectare extraído do artigo)
    - b = theta * P (coeficiente de rendimentos decrescentes)
    """
    params = {}
    for c, v in data_dict.items():
        P = float(v['P'])
        a = P
        b = theta * P
        params[c] = {'a': a, 'b': b}
    return params

def compute_optimum_unconstrained(a, b):
    """
    Calcula o ponto ótimo x* usando derivadas
    
    L(x) = ax - bx²
    L'(x) = a - 2bx = 0
    x* = a / (2b)
    
    Retorna: (x*, L(x*), tipo)
    """
    x_opt = a / (2.0 * b)
    L_opt = a * x_opt - b * (x_opt ** 2)
    
    # Teste da segunda derivada
    # L''(x) = -2b
    segunda_derivada = -2 * b
    
    if segunda_derivada < 0:
        tipo = "Máximo"
    elif segunda_derivada > 0:
        tipo = "Mínimo"
    else:
        tipo = "Ponto de Inflexão"
    
    return {
        'x_otimo': x_opt,
        'lucro_otimo': L_opt,
        'tipo': tipo,
        'segunda_derivada': segunda_derivada
    }

def compute_profit_at_area(a, b, A):
    """
    Calcula o lucro para uma área específica A
    L(A) = aA - bA²
    """
    return a * A - b * (A ** 2)

def analyze_with_sympy(a, b, A_max=10):
    """
    Análise completa usando SymPy (obrigatório no projeto)
    
    Retorna análise matemática detalhada com derivadas
    """
    x = sp.Symbol('x', real=True, positive=True)
    
    # Função lucro
    L = a * x - b * x**2
    
    # Primeira derivada
    L_prime = sp.diff(L, x)
    
    # Segunda derivada
    L_double_prime = sp.diff(L_prime, x)
    
    # Pontos críticos (L' = 0)
    pontos_criticos = sp.solve(L_prime, x)
    
    # Análise de cada ponto crítico
    analise = {
        'funcao': str(L),
        'primeira_derivada': str(L_prime),
        'segunda_derivada': str(L_double_prime),
        'pontos_criticos': [float(p) for p in pontos_criticos if p.is_real and p > 0],
        'classificacao': []
    }
    
    for pc in pontos_criticos:
        if pc.is_real and pc > 0:
            valor_segunda = float(L_double_prime.subs(x, pc))
            lucro_no_ponto = float(L.subs(x, pc))
            
            if valor_segunda < 0:
                tipo = "MÁXIMO"
            elif valor_segunda > 0:
                tipo = "MÍNIMO"
            else:
                tipo = "PONTO DE INFLEXÃO"
            
            analise['classificacao'].append({
                'ponto': float(pc),
                'lucro': lucro_no_ponto,
                'tipo': tipo,
                'segunda_derivada': valor_segunda
            })
    
    return analise

def generate_profit_plot(profits_dict, A):
    """
    Gera gráfico de barras comparando lucros
    """
    names = list(profits_dict.keys())
    vals = [profits_dict[n] for n in names]

    plt.figure(figsize=(10,6))
    bars = plt.bar(names, vals, color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'])
    
    plt.ylabel(f'Lucro (R$)', fontsize=12, fontweight='bold')
    plt.xlabel('Cultura', fontsize=12, fontweight='bold')
    plt.title(f'Lucro Estimado por Cultura para A={A} ha', fontsize=14, fontweight='bold')
    
    # Adiciona valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'R$ {height:,.0f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    plt.close()
    return buf

def generate_optimization_plot(a, b, A_constraint=5):
    """
    Gera gráfico da função L(x) mostrando o ponto ótimo
    """
    x_vals = np.linspace(0, A_constraint * 2, 200)
    L_vals = a * x_vals - b * (x_vals ** 2)
    
    # Ponto ótimo
    x_opt = a / (2 * b)
    L_opt = a * x_opt - b * (x_opt ** 2)
    
    # Ponto na restrição
    L_constraint = a * A_constraint - b * (A_constraint ** 2)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, L_vals, 'b-', linewidth=2, label='L(x) = ax - bx²')
    
    # Ponto ótimo
    plt.plot(x_opt, L_opt, 'ro', markersize=12, label=f'Ótimo: x*={x_opt:.2f}ha')
    
    # Ponto na restrição
    plt.plot(A_constraint, L_constraint, 'gs', markersize=12, 
             label=f'Restrição: A={A_constraint}ha')
    
    # Linhas de referência
    plt.axvline(x_opt, color='r', linestyle='--', alpha=0.5)
    plt.axhline(L_opt, color='r', linestyle='--', alpha=0.5)
    
    plt.xlabel('Área (hectares)', fontsize=12, fontweight='bold')
    plt.ylabel('Lucro (R$)', fontsize=12, fontweight='bold')
    plt.title('Análise de Otimização - Função Lucro', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    plt.close()
    return buf

def statsmodels_demo():
    np.random.seed(0)
    x = np.linspace(1,10,10)
    y = 5 * x + np.random.normal(0, 2, size=x.shape)
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()
    return model.summary()

def pycaret_demo(df, target):
    if not PYC_AVAILABLE:
        return 'pycaret não disponível'
    s = pyc_setup(df, target=target, silent=True, html=False)
    best = compare_models()
    return best