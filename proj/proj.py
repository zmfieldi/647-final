import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad

class FreshDataPricing:
    def __init__(self, T, f, C, max_K=20):
        self.T = T
        self.f = f
        self.C = C
        self.max_K = max_K
    
    def F(self, x):
        return quad(self.f, 0, x)[0]
    
    def DF(self, x, y):
        def integrand(t):
            return self.f(t + y) - self.f(t)
        
        return quad(integrand, 0, x)[0]
    
    def optimal_time_dependent_pricing(self):
        price = self.DF(self.T/2, self.T/2)
        def price_function(t):
            return price
        
        optimal_update_time = self.T/2
        destination_cost = 2 * self.F(self.T/2) + price
        source_profit = price - self.C(1)
        social_cost = 2 * self.F(self.T/2) + self.C(1)
        
        return {
            'pricing_scheme': 'time-dependent',
            'price_function': price_function,
            'optimal_update_times': [optimal_update_time],
            'K': 1,
            'destination_cost': destination_cost,
            'source_profit': source_profit,
            'social_cost': social_cost
        }
    
    def optimal_quantity_based_pricing(self):
        #  Find opt K
        best_K = 0
        min_cost = float('inf')
        
        for K in range(0, self.max_K + 1):
            x = self.T / (K + 1)
            total_cost = (K + 1) * self.F(x) + self.C(K)
            
            if total_cost < min_cost:
                min_cost = total_cost
                best_K = K
        
        #  Optimal pricing scheme
        K_star = best_K
        x_star = self.T / (K_star + 1)
        p_q = [0] * (K_star + 1)
        
        cumulative_price = 0
        for k in range(1, K_star):
            p_q[k] = self.F(self.T) - (k + 1) * self.F(self.T / (k + 1)) - cumulative_price + 0.01
            cumulative_price += p_q[k]
        
        if K_star >= 1:
            p_q[K_star] = self.F(self.T) - (K_star + 1) * self.F(self.T / (K_star + 1)) - cumulative_price
        
        #  Opt update times
        update_times = [i * x_star for i in range(1, K_star + 1)]
        
        #  Costs
        destination_cost = (K_star + 1) * self.F(x_star) + sum(p_q[1:])
        source_profit = sum(p_q[1:]) - self.C(K_star)
        social_cost = (K_star + 1) * self.F(x_star) + self.C(K_star)
        
        return {
            'pricing_scheme': 'quantity-based',
            'price_function': lambda k: p_q[k] if 0 <= k <= K_star else float('inf'),
            'prices': p_q[1:],  
            'optimal_update_times': update_times,
            'K': K_star,
            'destination_cost': destination_cost,
            'source_profit': source_profit,
            'social_cost': social_cost
        }
    
    def compare_pricing_schemes(self):
        tdp = self.optimal_time_dependent_pricing()
        qbp = self.optimal_quantity_based_pricing()
        
        return {
            'time_dependent': tdp,
            'quantity_based': qbp,
            'profit_comparison': {
                'time_dependent': tdp['source_profit'],
                'quantity_based': qbp['source_profit'],
                'difference': qbp['source_profit'] - tdp['source_profit'],
                'ratio': qbp['source_profit'] / tdp['source_profit'] if tdp['source_profit'] != 0 else float('inf')
            },
            'social_cost_comparison': {
                'time_dependent': tdp['social_cost'],
                'quantity_based': qbp['social_cost'],
                'difference': tdp['social_cost'] - qbp['social_cost'],
                'ratio': tdp['social_cost'] / qbp['social_cost'] if qbp['social_cost'] != 0 else float('inf')
            }
        }

