import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# optional libs
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler


# Dados extraídos do artigo
DEFAULT_DATA = {
    'Milho': {'P': 70262.27},
    'Feijao': {'P': 40593.61},
    'Macaxeira': {'P': 77468.64},
    'Batata-doce': {'P': 75692.15}
}

def calibrate_b_theta(data_dict, theta=0.05):
    params = {}
    for c, v in data_dict.items():
        P = float(v['P'])
        a = P
        b = theta * P
        params[c] = {'a': a, 'b': b}
    return params

def compute_optimum_unconstrained(a, b):
    return a / (2.0 * b)

def compute_profit_at_area(a, b, A):
    return a * A - b * (A ** 2)

def generate_profit_plot(profits_dict, A):
    names = list(profits_dict.keys())
    vals = [profits_dict[n] for n in names]

    plt.figure(figsize=(8,5))
    sns.barplot(x=names, y=vals)
    plt.ylabel(f'Lucro (R$) em A={A} ha')
    plt.title(f'Lucro estimado por cultura para A={A} ha')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
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


