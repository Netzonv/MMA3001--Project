import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_smoothing_spline, UnivariateSpline

def apply_spline_approximation(x_points, y_points, lam=1.0, s=50, num_eval_points=500):
    """
    Fits a smoothing spline to the provided data points and returns both the fitted model
    and evaluated points over a dense grid for smooth plotting.
    
    Parameters:
    -----------
    x_points : array-like
        The independent variable values (e.g., hours/time indices).
    y_points : array-like
        The dependent variable values (e.g., average occupancy counts).
    lam : float, optional (default=1.0)
        Smoothness parameter for make_smoothing_spline (higher = smoother).
    s : float, optional (default=50)
        Smoothing factor fallback parameter for UnivariateSpline if make_smoothing_spline is unavailable.
    num_eval_points : int, optional (default=500)
        Number of points on the dense timeline grid to evaluate for smooth visualization.
        
    Returns:
    --------
    model : spline object
        The fitted spline model (can be called like model(x)).
    x_dense : ndarray
        The dense evaluation points along the X-axis.
    y_dense : ndarray
        The corresponding evaluated smooth spline values along the Y-axis.
    """
    # Ensure inputs are numpy arrays
    x_points = np.asarray(x_points)
    y_points = np.asarray(y_points)
    
    # Check for the modern scipy make_smoothing_spline module
    try:
        from scipy.interpolate import make_smoothing_spline
        HAS_SPLINE = True
    except ImportError:
        HAS_SPLINE = False
        
    # Fit the spline model
    if HAS_SPLINE:
        model = make_smoothing_spline(x_points, y_points, lam=lam)
        print(f"Fitted modern make_smoothing_spline with lam={lam}")
    else:
        model = UnivariateSpline(x_points, y_points, s=s)
        print(f"Fitted UnivariateSpline fallback with s={s}")
        
    # Generate dense grid and evaluate
    x_dense = np.linspace(x_points.min(), x_points.max(), num_eval_points)
    y_dense = model(x_dense)
    
    return model, x_dense, y_dense
