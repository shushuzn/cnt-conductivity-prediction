# -*- coding: utf-8 -*-
"""
Active Learning Simulator for LIG Conductivity Optimization

Tests active learning algorithm performance before real experimental platform
Simulates LIG conductivity prediction scenario

Dependencies:
    pip install scikit-learn scipy numpy matplotlib
"""

import numpy as np
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 70)
print("Active Learning Simulator - LIG Conductivity Optimization")
print("=" * 70)

# 1. Define true function (simulate LIG conductivity vs process parameters)
print("\n[1/5] Defining true function...")

def true_lig_conductivity(X):
    """
    Simulate LIG conductivity vs process parameters
    
    Parameters:
    X: [Power density (J/cm2), Scan speed (mm/s), Pass count]
    
    Returns:
    Conductivity (S/m)
    """
    P = X[:, 0]  # Power density
    v = X[:, 1]  # Scan speed
    n = X[:, 2]  # Pass count
    
    # Simulate true relationship (physics-based)
    cond_P = np.exp(-((P - 20) ** 2) / 200)  # Optimal power density
    cond_v = np.exp(-v / 50)  # Speed negative correlation
    cond_n = 1 - np.exp(-n / 3)  # Pass count positive (saturating)
    
    conductivity = 1e6 * cond_P * cond_v * cond_n
    
    # Add noise
    noise = np.random.normal(0, 0.1, len(X))
    conductivity *= (1 + noise)
    
    return conductivity

# Generate candidate space
np.random.seed(42)
n_candidates = 1000

X_candidate = np.random.rand(n_candidates, 3)
X_candidate[:, 0] *= 40 + 5    # Power density: 5-45 J/cm2
X_candidate[:, 1] *= 80 + 10   # Scan speed: 10-90 mm/s
X_candidate[:, 2] *= 8 + 1     # Pass count: 1-9

y_candidate = true_lig_conductivity(X_candidate)

print(f"  Candidate space: {n_candidates} samples")
print(f"  Power density: {X_candidate[:, 0].min():.1f} - {X_candidate[:, 0].max():.1f} J/cm2")
print(f"  Scan speed: {X_candidate[:, 1].min():.1f} - {X_candidate[:, 1].max():.1f} mm/s")
print(f"  Pass count: {X_candidate[:, 2].min():.1f} - {X_candidate[:, 2].max():.1f}")
print(f"  Conductivity: {y_candidate.min():.2e} - {y_candidate.max():.2e} S/m")

# 2. Initialize training set (simulate initial literature data)
print("\n[2/5] Initializing training set...")

n_initial = 20
initial_idx = np.random.choice(n_candidates, n_initial, replace=False)
X_train = X_candidate[initial_idx].copy()
y_train = y_candidate[initial_idx].copy()

remaining_idx = np.setdiff1d(np.arange(n_candidates), initial_idx)
X_remaining = X_candidate[remaining_idx].copy()
y_remaining = y_candidate[remaining_idx].copy()

print(f"  Initial training: {n_initial} samples")
print(f"  Validation: {len(remaining_idx)} samples")

# 3. Active learning loop
print("\n[3/5] Active learning loop...")

kernel = ConstantKernel(1.0) * RBF(length_scale=[1.0, 1.0, 1.0]) + WhiteKernel(0.1)

history = {
    'iteration': [],
    'n_samples': [],
    'r2_score': [],
    'best_conductivity': []
}

n_iterations = 20

for iteration in range(n_iterations):
    # Train GP model
    gp = GaussianProcessRegressor(
        kernel=kernel,
        n_restarts_optimizer=10,
        random_state=42,
        normalize_y=True
    )
    gp.fit(X_train, y_train)
    
    # Predict + uncertainty
    y_pred, y_std = gp.predict(X_remaining, return_std=True)
    
    # Expected Improvement acquisition function
    y_best = y_train.max()
    ei = (y_pred - y_best) * norm.cdf((y_pred - y_best) / (y_std + 1e-6)) + \
         (y_std + 1e-6) * norm.pdf((y_pred - y_best) / (y_std + 1e-6))
    
    # Select next point
    next_idx = np.argmax(ei)
    X_next = X_remaining[next_idx:next_idx+1]
    y_next = y_remaining[next_idx:next_idx+1]
    
    # Update training set
    X_train = np.vstack([X_train, X_next])
    y_train = np.append(y_train, y_next[0])
    
    # Remove from remaining
    X_remaining = np.delete(X_remaining, next_idx, axis=0)
    y_remaining = np.delete(y_remaining, next_idx, axis=0)
    
    # Record history
    y_pred_all = gp.predict(X_candidate)
    r2 = r2_score(y_candidate, y_pred_all)
    
    history['iteration'].append(iteration)
    history['n_samples'].append(len(X_train))
    history['r2_score'].append(r2)
    history['best_conductivity'].append(y_train.max())
    
    print(f"  Iteration {iteration+1:2d}/{n_iterations}: "
          f"R2 = {r2:.3f}, Best = {y_train.max():.2e} S/m")

# 4. Visualization
print("\n[4/5] Generating plots...")

figures_dir = Path("D:/OpenClaw/workspace/11-research/cnt-research/figures")
figures_dir.mkdir(parents=True, exist_ok=True)

# Plot 1: R2 improvement
fig1, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
ax1.plot(history['iteration'], history['r2_score'], 'b-o', linewidth=2, markersize=6)
ax1.axhline(y=0.90, color='r', linestyle='--', linewidth=2, label='Target R2 = 0.90')
ax1.set_xlabel("Active Learning Iteration", fontsize=12)
ax1.set_ylabel("R2 Score", fontsize=12)
ax1.set_title("Active Learning Performance Improvement", fontsize=14)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(figures_dir / "active_learning_r2_improvement.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] R2 improvement plot saved")

# Plot 2: Best conductivity
fig2, ax2 = plt.subplots(figsize=(10, 6), dpi=300)
ax2.plot(history['iteration'], history['best_conductivity'], 'g-o', linewidth=2, markersize=6)
ax2.set_xlabel("Active Learning Iteration", fontsize=12)
ax2.set_ylabel("Best Conductivity (S/m)", fontsize=12)
ax2.set_title("Best Conductivity Discovery", fontsize=14)
ax2.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(figures_dir / "active_learning_best_conductivity.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] Best conductivity plot saved")

# Plot 3: Samples vs R2
fig3, ax3 = plt.subplots(figsize=(10, 6), dpi=300)
ax3.plot(history['n_samples'], history['r2_score'], 'm-o', linewidth=2, markersize=6)
ax3.set_xlabel("Number of Training Samples", fontsize=12)
ax3.set_ylabel("R2 Score", fontsize=12)
ax3.set_title("Model Performance vs Training Data Size", fontsize=14)
ax3.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(figures_dir / "active_learning_samples_vs_r2.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  [OK] Samples vs R2 plot saved")

# 5. Summary
print("\n[5/5] Summary...")

print("\n" + "=" * 70)
print("[OK] Active Learning Simulation Complete!")
print("=" * 70)

print(f"\nInitial:")
print(f"  Training samples: {n_initial}")
print(f"  Initial R2: {history['r2_score'][0]:.3f}")
print(f"  Initial best: {history['best_conductivity'][0]:.2e} S/m")

print(f"\nFinal (after 20 iterations):")
print(f"  Training samples: {len(X_train)}")
print(f"  Final R2: {history['r2_score'][-1]:.3f}")
print(f"  Final best: {history['best_conductivity'][-1]:.2e} S/m")

print(f"\nBest parameters discovered:")
best_idx = np.argmax(y_train)
best_params = X_train[best_idx]
best_value = y_train[best_idx]
print(f"  Power density: {best_params[0]:.1f} J/cm2")
print(f"  Scan speed: {best_params[1]:.1f} mm/s")
print(f"  Pass count: {best_params[2]:.1f}")
print(f"  Conductivity: {best_value:.2e} S/m")

print(f"\nFigures saved to: {figures_dir}")
print(f"\nNext steps:")
print(f"  1. Analyze active learning effectiveness")
print(f"  2. Tune acquisition function (EI/UCB/PI)")
print(f"  3. Prepare real experimental platform")
print(f"  4. Integrate into actual system")
