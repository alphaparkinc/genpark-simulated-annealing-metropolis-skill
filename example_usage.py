from client import SimulatedAnnealingOptimizer

def main():
    sa = SimulatedAnnealingOptimizer()
    res = sa.optimize(lambda p: (p[0] - 3.5)**2 + (p[1] + 2.0)**2, [0.0, 0.0])
    print("Simulated Annealing Verification:")
    print(f"Optimal Cost: {res['best_cost']}")
    print(f"Optimal State: {res['best_state']} (Target: [3.5, -2.0])")

if __name__ == "__main__":
    main()
