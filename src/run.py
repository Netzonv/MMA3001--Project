import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import (
    make_interp_spline,
    CubicSpline,
    PchipInterpolator,
    Akima1DInterpolator
)

# runs 4 different types of splines onto the data
if 'count_array' in globals() and 'occupancy_count_array' in globals():
   fitted_models = compare_spline_methods(count_array, occupancy_count_array, lam=1.0)
else:
    print("Demo skipped: 'count_array' or 'occupancy_count_array' variables are not populated.")

import time
import tracemalloc
from scipy.interpolate import make_smoothing_spline, UnivariateSpline

# runs validation test of smoothing spline against Week 2 raw data
if 'fitted_models' in globals() and 'occupancy_count_week2' in globals() and 'timestamps_week2' in globals():
    # Evaluate the smoothing spline model against the second week
    evaluate_model_on_week2(
        model=fitted_models['smoothing'],
        week2_data=occupancy_count_week2,
        week2_timestamps=timestamps_week2,
        label="Smoothing Spline"
    )
else:
    print("Demo skipped: required variables or models are not initialized.")

# returns performance metric depending on the sample factor - factor of 2 means 2x less data to model from
optimize_spline_fitting(count_array, occupancy_count_array, downsample_factor=2, lam=1.0, s=50)

