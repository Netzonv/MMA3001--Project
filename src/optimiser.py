def optimize_spline_fitting(x_points, y_points, downsample_factor=1, lam=1.0, s=50):
    """
    Fits a smoothing spline with performance optimizations focusing on downsampling.
    
    Parameters:
    -----------
    x_points : array-like
        Original independent variable values (e.g. hours).
    y_points : array-like
        Original dependent variable values (e.g. occupancy counts).
    downsample_factor : int, optional (default=1)
        Downsampling step size (e.g., 2 selects every 2nd point).
    lam : float, optional (default=1.0)
        Smoothing parameter for make_smoothing_spline.
    s : float, optional (default=50)
        Smoothing factor fallback parameter for UnivariateSpline.
        
    Returns:
    --------
    model : spline object
        The optimized fitted spline model.
    metrics : dict
        Dictionary containing 'computational_time_ms', 'peak_memory_kb', and 'fit_mae'.
    """
    import time
    import tracemalloc
    import numpy as np
    from scipy.interpolate import make_smoothing_spline, UnivariateSpline

    # Convert input list/series to numpy arrays
    x_arr = np.asarray(x_points)
    y_arr = np.asarray(y_points)

    # Apply Downsampling Optimization if requested
    if downsample_factor > 1:
        x_arr = x_arr[::downsample_factor]
        y_arr = y_arr[::downsample_factor]

    # Determine smoothing spline availability
    try:
        from scipy.interpolate import make_smoothing_spline
        has_modern = True
    except ImportError:
        from scipy.interpolate import UnivariateSpline
        has_modern = False

    # Start performance tracking
    tracemalloc.start()
    start_time = time.perf_counter()

    # Perform the model fitting
    if has_modern:
        model = make_smoothing_spline(x_arr, y_arr, lam=lam)
    else:
        model = UnivariateSpline(x_arr, y_arr, s=s)

    end_time = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Calculate metrics
    time_ms = (end_time - start_time) * 1000
    mem_kb = peak_mem / 1024
    
    # Calculate error relative to the original un-downsampled data points
    predictions = model(x_points)
    mae = np.mean(np.abs(y_points - predictions))

    metrics = {
        'computational_time_ms': time_ms,
        'peak_memory_kb': mem_kb,
        'fit_mae': mae
    }

    print(f"=== Optimization Results (Downsample: {downsample_factor}x) ===")
    print(f"Computational Time : {time_ms:.4f} ms")
    print(f"Peak Memory Usage  : {mem_kb:.4f} KB")
    print(f"Fit MAE            : {mae:.4f} occupants")

    return model, metrics
