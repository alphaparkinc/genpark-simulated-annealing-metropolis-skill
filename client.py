"""Simulated Annealing Global Search Engine
100% Python Standard Library (math, random).
"""

import math
import random

class SimulatedAnnealingOptimizer:
    """Thermodynamic global energy minimization engine."""
    def __init__(self, init_temp=100.0, cooling_rate=0.95, min_temp=1e-3, steps_per_temp=10):
        self.init_temp = init_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.steps_per_temp = steps_per_temp

    def optimize(self, cost_fn, init_state, step_size=0.5):
        current_state = list(init_state)
        current_cost = cost_fn(current_state)
        best_state = list(current_state)
        best_cost = current_cost
        temp = self.init_temp

        while temp > self.min_temp:
            for _ in range(self.steps_per_temp):
                neighbor = [x + random.gauss(0, step_size) for x in current_state]
                neighbor_cost = cost_fn(neighbor)
                delta = neighbor_cost - current_cost

                if delta < 0 or random.random() < math.exp(-min(delta / max(1e-9, temp), 50.0)):
                    current_state = neighbor
                    current_cost = neighbor_cost
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_state = list(current_state)

            temp *= self.cooling_rate

        return {
            "best_cost": round(best_cost, 6),
            "best_state": [round(x, 4) for x in best_state]
        }
