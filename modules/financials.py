import numpy as np
import pandas as pd

def calculate_roi(ingresos, costos):
    return (ingresos - costos) / costos * 100 if costos > 0 else 0

def monte_carlo_simulation(pedidos, precio, costos_base, dias, food_cost_pct, n_sim=1000):
    ingresos = []
    for _ in range(n_sim):
        p = np.random.normal(pedidos, pedidos * 0.2)
        pr = np.random.normal(precio, precio * 0.1)
        c = np.random.normal(costos_base, costos_base * 0.15)
        d = np.random.normal(dias, dias * 0.1)
        fc = np.random.normal(food_cost_pct, food_cost_pct * 0.1) / 100
        ingresos_sim = p * pr * d * 4 * (1 - fc) - c
        ingresos.append(ingresos_sim)
    return pd.DataFrame({"Ingresos": ingresos})
