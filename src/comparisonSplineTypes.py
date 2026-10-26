import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import (
    make_interp_spline,
    CubicSpline,
    PchipInterpolator,
    Akima1DInterpolator
)

def compare_spline_methods(x_points, y_points, lam=1.0, s=50, num_eval_points=500):
    """
    Fits and compares four different interpolation/smoothing spline techniques:
    1. Linear Spline
    2. Cubic Spline
    3. PCHIP Spline (Monotone-preserving)
    4. Smoothing Spline
    
    Plots the comparison side-by-side and returns the fitted models.
    
    Parameters:
    -----------
    x_points : array-like
        The X coordinates of the data (e.g., hourly indices).
    y_points : array-like
        The Y coordinates of the data (e.g., occupancy counts).
    lam : float, optional (default=1.0)
        Smoothing parameter for make_smoothing_spline.
    s : float, optional (default=50)
        Smoothing factor fallback parameter for UnivariateSpline.
    num_eval_points : int, optional (default=500)
        Number of evaluation points over the dense timeline grid.
        
    Returns:
    --------
    models : dict
        A dictionary containing the fitted model objects:
        {'linear': linear_model, 'cubic': cubic_model, 'pchip': pchip_model, 'smoothing': smoothing_model}
    """
    x_points = np.asarray(x_points)
    y_points = np.asarray(y_points)
    
    # 1. Fit the models
    linear_model = make_interp_spline(x_points, y_points, k=1)
    cubic_model = CubicSpline(x_points, y_points)
    pchip_model = PchipInterpolator(x_points, y_points)
    
    # Determine smoothing spline availability
    try:
        from scipy.interpolate import make_smoothing_spline
        smoothing_model = make_smoothing_spline(x_points, y_points, lam=lam)
        has_modern = True
    except ImportError:
        from scipy.interpolate import UnivariateSpline
        smoothing_model = UnivariateSpline(x_points, y_points, s=s)
        has_modern = False
        
    # 2. Set up dense evaluation timeline
    x_dense = np.linspace(x_points.min(), x_points.max(), num_eval_points)
    
    # 3. Create comparative plots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharex=True, sharey=True)
    axes = axes.ravel()
    
    # Define plot details
    methods = [
        ("Linear Spline", linear_model, 'tab:blue', "Exact but jagged"),
        ("Cubic Spline", cubic_model, 'tab:orange', "Can overshoot/oscillate"),
        ("PCHIP Spline", pchip_model, 'tab:green', "Smooth & obeys local bounds"),
        ("Smoothing Spline", smoothing_model, 'tab:red', f"Extracts overall trend (lam={lam if has_modern else s})")
    ]
    
    for i, (name, model, color, notes) in enumerate(methods):
        ax = axes[i]
        ax.plot(x_points, y_points, 'k.', alpha=0.4, label="Raw Data")
        ax.plot(x_dense, model(x_dense), color=color, linewidth=2, label=name)
        
        # Calculate MAE at training points
        mae = np.mean(np.abs(y_points - model(x_points)))
        
        ax.set_title(f"{name}\n({notes}) | MAE: {mae:.4f}", fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, linestyle='--', alpha=0.5)
        
    fig.supxlabel("Timeline Index (Hours)", fontsize=12)
    fig.supylabel("Occupant Metrics", fontsize=12)
    fig.suptitle("Comparison of Spline Approximation and Interpolation Techniques", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    models = {
        'linear': linear_model,
        'cubic': cubic_model,
        'pchip': pchip_model,
        'smoothing': smoothing_model
    }
    return models
