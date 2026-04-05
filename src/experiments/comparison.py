import matplotlib.pyplot as plt
import random
from src.algorithms.hill_climbing import HillClimbing

def compare_algorithms():
    items = [random.randint(1, 10) for _ in range(60)]
    capacity = 10

    hc = HillClimbing(capacity)

    hc_sol, hc_hist = hc.optimize(items, max_iter=500)

    print("Hill Climbing bins:", len(hc_sol.bins))

    plt.figure()
    plt.plot(hc_hist, label="Hill Climbing")
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.title("Algorithm Comparison")
    plt.legend()
    plt.grid()

    plt.savefig("comparison.png")
    plt.show()
