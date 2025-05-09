import numpy as np
import matplotlib.pyplot as plt
from proj import FreshDataPricing

class FreshDataVisualizations:

    def __init__(self, pricing_model):
        self.pricing = pricing_model
        self.T = pricing_model.T
        self.f = pricing_model.f
        self.C = pricing_model.C
        
    def plot_age_of_information(self):
        tdp = self.pricing.optimal_time_dependent_pricing()
        qbp = self.pricing.optimal_quantity_based_pricing()
        
     
        plt.figure(figsize=(10, 6))
        
        
        t = np.linspace(0, self.T, 1000)
        
        #  Plot AoI for time-dependent pricing 
        aoi_tdp = np.minimum(t, np.abs(t - self.T/2) + self.T/2)
        plt.plot(t, aoi_tdp, 'b-', label='Time-Dependent Pricing')
        
        #  Plot AoI for quantity-based pricing 
        K_star = qbp['K']
        update_interval = self.T / (K_star + 1)
        update_times = [i * update_interval for i in range(1, K_star + 1)]
        
        aoi_qbp = np.zeros_like(t)
        for i, ti in enumerate(t):
            most_recent = 0
            for upd in update_times:
                if upd <= ti:
                    most_recent = upd
            aoi_qbp[i] = ti - most_recent
        
        plt.plot(t, aoi_qbp, 'r-', label='Quantity-Based Pricing')
        
        #  Plot no-update baseline
        plt.plot(t, t, 'g--', label='No Update')
        
        #  Add update markers
        if K_star > 0:
            plt.scatter(update_times, [0] * K_star, color='r', s=80, zorder=3, label='_nolegend_')
        plt.scatter([self.T/2], [0], color='b', s=80, zorder=3, label='_nolegend_')
        
        plt.xlabel('Time')
        plt.ylabel('Age of Information (AoI)')
        plt.title('Age of Information Over Time')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        return plt.gcf()

    def plot_cost_comparison(self):

        # Get results
        tdp = self.pricing.optimal_time_dependent_pricing()
        qbp = self.pricing.optimal_quantity_based_pricing()
        
        # Calculate costs for no-update
        no_update_aoi_cost = self.pricing.F(self.T)
        no_update_source_profit = 0
        no_update_social_cost = no_update_aoi_cost
        
        # Data for bar chart
        labels = ['Time-Dependent', 'Quantity-Based', 'No Update']
        
        # Cost data
        destination_costs = [tdp['destination_cost'], qbp['destination_cost'], no_update_aoi_cost]
        source_profits = [tdp['source_profit'], qbp['source_profit'], no_update_source_profit]
        social_costs = [tdp['social_cost'], qbp['social_cost'], no_update_social_cost]
        
        # Create bar chart
        x = np.arange(len(labels))
        width = 0.25
        
        fig, ax = plt.subplots(figsize=(10, 6))
        rects1 = ax.bar(x - width, destination_costs, width, label="Destination's Cost")
        rects2 = ax.bar(x, source_profits, width, label="Source's Profit")
        rects3 = ax.bar(x + width, social_costs, width, label="Social Cost")
        
        ax.set_xlabel('Pricing Scheme')
        ax.set_ylabel('Cost / Profit')
        ax.set_title('Comparison of Costs and Profits')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        
        # Add value labels on bars
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.1f}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')
        
        autolabel(rects1)
        autolabel(rects2)
        autolabel(rects3)
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()
    
    def plot_differential_cost(self):
        """Plot differential aggregate AoI cost function"""
        # Create figure
        plt.figure(figsize=(8, 5))
        
        # Generate values for x and y
        x_vals = np.linspace(0.1, self.T/2, 100)
        
        # Generate differential costs for fixed y
        fixed_y = self.T/4
        df_vals = [self.pricing.DF(x, fixed_y) for x in x_vals]
        
        plt.plot(x_vals, df_vals, 'b-', linewidth=2)
        
        plt.xlabel('x')
        plt.ylabel('DF(x, y)')
        plt.title(f'Differential Aggregate AoI Cost Function (y = {fixed_y:.1f})')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()
    
    def plot_optimal_pricing(self):
       
        # Get results
        qbp = self.pricing.optimal_quantity_based_pricing()
        
        K_star = qbp['K']
        prices = qbp['prices']
        
        if K_star == 0:
            plt.figure(figsize=(8, 5))
            plt.text(0.5, 0.5, "No updates in optimal solution", 
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=14)
            plt.axis('off')
            return plt.gcf()
        

        plt.figure(figsize=(8, 5))
        
        
        plt.bar(range(1, K_star+1), prices, color='skyblue')
        
        plt.xlabel('k-th Update')
        plt.ylabel('Price')
        plt.title('Optimal Quantity-Based Pricing Scheme')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()
    
    def plot_marginal_cost_revenue(self):
        plt.figure(figsize=(8, 5))
        
        #  K values
        K_vals = np.linspace(0.1, self.pricing.max_K, 100)
        
        marginal_revenue = []
        for K in K_vals:
            x = self.T / (K + 1)
            mr = self.f(x) * x - self.pricing.F(x)
            marginal_revenue.append(mr)
        
        #  Calculate marginal cost for each K
        marginal_cost = []
        K_int = np.arange(0, self.pricing.max_K+1)
        cost_vals = [self.C(k) for k in K_int]
        
        #  Cost Func
        for K in K_vals:
            K_floor = int(np.floor(K))
            K_ceil = int(np.ceil(K))
            
            if K_floor == K_ceil:
                mc = (cost_vals[min(K_ceil+1, len(cost_vals)-1)] - cost_vals[max(K_floor-1, 0)]) / 2
            else:
                mc = cost_vals[K_ceil] - cost_vals[K_floor]
            
            marginal_cost.append(mc)
        
        plt.plot(K_vals, marginal_revenue, 'b-', label='Marginal Revenue')
        plt.plot(K_vals, marginal_cost, 'r-', label='Marginal Cost')
        
        #  Find intersection point
        intersection_idx = np.argmin(np.abs(np.array(marginal_revenue) - np.array(marginal_cost)))
        K_intersect = K_vals[intersection_idx]
        
        plt.axvline(x=K_intersect, color='g', linestyle='--', 
                   label=f'Threshold K = {K_intersect:.1f}')
        
        plt.xlabel('Number of Updates K')
        plt.ylabel('Marginal Revenue/Cost')
        plt.title('Marginal Revenue and Cost Analysis')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        return plt.gcf()
