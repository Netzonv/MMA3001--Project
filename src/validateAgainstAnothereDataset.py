def evaluate_model_on_week2(model, week2_data, week2_timestamps, label="Spline Model"): 
    """
    Evaluates a fitted spline model against the second week's actual occupancy data.
    
    Parameters:
    -----------
    model : spline object
        The fitted model (e.g., from fitted_models['smoothing'] or fitted_models['pchip']).
    week2_data : array-like
        The actual occupancy counts for Week 2 (must be length 168).
    week2_timestamps : array-like (datetime)
        The timestamps corresponding to Week 2.
    label : str, optional
        The name of the model being evaluated (for labels and legends).
        
    Returns:
    --------
    mae : float
        Mean Absolute Error of the model's predictions against actual Week 2 data.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    # Ensure inputs are numpy arrays
    y_actual = np.asarray(week2_data)
    t_actual = np.asarray(week2_timestamps)
    
    # Map Week 2 timeline to the 0-167 fitting scale
    x_eval = np.arange(len(y_actual))
    
    # Predict using the provided model
    y_pred = model(x_eval)
    
    # Calculate Mean Absolute Error (MAE)
    mae = np.mean(np.abs(y_actual - y_pred))
    
    # Create a dense evaluation grid for smooth visualization curves
    x_dense = np.linspace(x_eval.min(), x_eval.max(), 500)
    y_dense = model(x_dense)
    
    # Map evaluated points back to timestamps
    start_time = t_actual[0]
    end_time = t_actual[-1]
    time_deltas = (end_time - start_time) * (x_dense / x_eval.max())
    dense_timestamps = start_time + time_deltas
    
    # Generate comparative plot
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(t_actual, y_actual, 'k.', alpha=0.5, label="Week 2 Actual Data")
    ax.plot(dense_timestamps, y_dense, color='tab:red', linewidth=2.5, label=f"{label} Projection")
    
    # Format X-axis to elegant day/date formats
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%A\n%b %d'))
    
    ax.set_xlabel("Week 2 Timeline", labelpad=10, fontsize=11)
    ax.set_ylabel("Number of Occupants", fontsize=11)
    ax.set_title(f"Evaluation: Comparing {label} against Week 2 Data (MAE: {mae:.3f} occupants)", fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    plt.show()
    
    print(f"=== Evaluation Metrics ({label}) ===")
    print(f"Mean Absolute Error (MAE): {mae:.4f} occupants")
    
    return mae

# --- Demo of the evaluation function ---
#if 'fitted_models' in globals() and 'occupancy_count_week2' in globals() and 'timestamps_week2' in globals():
    # Evaluate the smoothing spline model against the second week
#    evaluate_model_on_week2(
#        model=fitted_models['smoothing'], 
#        week2_data=occupancy_count_week2, 
#        week2_timestamps=timestamps_week2, 
#        label="Smoothing Spline"
#    )
#else:
#    print("Demo skipped: required variables or models are not initialized.")
