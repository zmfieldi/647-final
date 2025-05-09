import numpy as np
import matplotlib.pyplot as plt
from proj import FreshDataPricing
from main import FreshDataVisualizations
import os

def run_demo():
    #  Parameters
    T = 30  #
    
    #  AoI
    kappa = 1.5  
    f = lambda x: x**kappa
    print(f"   - Time horizon: T = {T} days")
    print(f"   - AoI cost function: f(Δ) = Δ^{kappa}")
    
    #  Operational cost 
    c = 6.0  
    C = lambda K: c * (K**3)
    print(f"   - Operational cost function: C(K) = {c} * K^3")

    pricing = FreshDataPricing(T, f, C)

    print("\n2. Computing optimal pricing schemes...")
    tdp = pricing.optimal_time_dependent_pricing()
    qbp = pricing.optimal_quantity_based_pricing()
    
    #  Display results for time-dependent pricing
    print("\n3. Time-Dependent Pricing Results:")
    print(f"   - Optimal update time: t = {tdp['optimal_update_times'][0]:.2f}")
    print(f"   - Price: {tdp['price_function'](0):.2f}")
    print(f"   - Source profit: {tdp['source_profit']:.2f}")
    print(f"   - Destination cost: {tdp['destination_cost']:.2f}")
    print(f"   - Social cost: {tdp['social_cost']:.2f}")
    
    #  Display results for quantity-based pricing
    print("\n4. Quantity-Based Pricing Results:")
    print(f"   - Optimal number of updates (K*): {qbp['K']}")
    print(f"   - Optimal update times: {[round(t, 2) for t in qbp['optimal_update_times']]}")
    print(f"   - Prices: {[round(p, 2) for p in qbp['prices']]}")
    print(f"   - Source profit: {qbp['source_profit']:.2f}")
    print(f"   - Destination cost: {qbp['destination_cost']:.2f}")
    print(f"   - Social cost: {qbp['social_cost']:.2f}")
    
    #  Compare pricing schemes
    print("\n5. Comparison:")
    profit_increase = qbp['source_profit'] - tdp['source_profit']
    social_cost_reduction = tdp['social_cost'] - qbp['social_cost']
    print(f"   - Profit increase with quantity-based pricing: {profit_increase:.2f} ({profit_increase/tdp['source_profit']*100:.1f}%)")
    print(f"   - Social cost reduction with quantity-based pricing: {social_cost_reduction:.2f} ({social_cost_reduction/tdp['social_cost']*100:.1f}%)")
    
    # Create visualization object
    viz = FreshDataVisualizations(pricing)

    print("\n6. Generating visualizations...")
    output_dir = "fresh_data_figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    #  Generate and save plots
    fig1 = viz.plot_age_of_information()
    fig1.savefig(f"{output_dir}/aoi_over_time.pdf", dpi=300, bbox_inches='tight')
    print(f"   - Saved Age of Information visualization")
    
    fig2 = viz.plot_cost_comparison()
    fig2.savefig(f"{output_dir}/cost_comparison.pdf", dpi=300, bbox_inches='tight')
    print(f"   - Saved Cost/Profit comparison visualization")
    
    fig3 = viz.plot_differential_cost()
    fig3.savefig(f"{output_dir}/differential_cost.pdf", dpi=300, bbox_inches='tight')
    print(f"   - Saved Differential Cost visualization")
    
    fig4 = viz.plot_optimal_pricing()
    fig4.savefig(f"{output_dir}/optimal_pricing.pdf", dpi=300, bbox_inches='tight')
    print(f"   - Saved Optimal Pricing visualization")
    
    fig5 = viz.plot_marginal_cost_revenue()
    fig5.savefig(f"{output_dir}/marginal_analysis.pdf", dpi=300, bbox_inches='tight')
    print(f"   - Saved Marginal Cost/Revenue visualization")
    
    print("\nDemo completed successfully. Figures saved to the 'fresh_data_figures' directory.")
    return {
        'time_dependent': tdp,
        'quantity_based': qbp,
    }

if __name__ == "__main__":
    run_demo()