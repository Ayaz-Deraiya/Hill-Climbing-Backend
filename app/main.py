import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import random

# Add project root to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algorithms.hill_climbing import HillClimbing
from src.algorithms.backtracking import BacktrackingBinPacking
from app.schemas import OptimizationRequest, OptimizationResult, BinResponse, BatchCompareRequest, BatchCompareResponse, BatchCompareItemResult, TestCaseResult
import time

app = FastAPI(title="Bin Packing AI API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def format_solution(solution, algorithm_name, history):
    bins = [
        BinResponse(items=b.items, used=b.used, capacity=b.capacity)
        for b in solution.bins
    ]
    return OptimizationResult(
        algorithm=algorithm_name,
        bins=bins,
        cost_history=history,
        num_bins=len(solution.bins),
        final_cost=solution.cost()
    )

@app.post("/optimize", response_model=OptimizationResult)
async def optimize(request: OptimizationRequest):
    if request.algorithm == "hc":
        solver = HillClimbing(request.capacity)
        solution, history = solver.optimize(request.items, max_iter=request.max_iter)
        return format_solution(solution, "Hill Climbing", history)
    else:
        raise HTTPException(status_code=400, detail="Invalid algorithm. Use 'hc'.")

@app.get("/random_items")
async def random_items(count: int = 20, min_val: int = 1, max_val: int = 10):
    return {"items": [random.randint(min_val, max_val) for _ in range(count)]}

def parse_batch_text(text: str):
    test_cases = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        if lines[i].lower().startswith("testcase"):
            name = lines[i].replace(":", "").strip()
            i += 1
            if i < len(lines):
                parts = lines[i].split()
                if len(parts) >= 2:
                    n = int(parts[0])
                    cap = int(parts[1])
                    i += 1
                    items = []
                    while i < len(lines) and len(items) < n and not lines[i].lower().startswith("testcase"):
                        curr_items = [int(x) for x in lines[i].split()]
                        items.extend(curr_items)
                        i += 1
                    test_cases.append({"name": name, "capacity": cap, "items": items[:n]})
                else:
                    i += 1
        else:
            i += 1
    return test_cases

@app.post("/compare-batch", response_model=BatchCompareResponse)
async def compare_batch(request: BatchCompareRequest):
    test_cases = parse_batch_text(request.batch_text)
    results = []
    
    for tc in test_cases:
        cap = tc["capacity"]
        items = tc["items"]
        
        hc_solver = HillClimbing(cap)
        start_hc = time.perf_counter()
        hc_sol, _ = hc_solver.optimize(items, max_iter=500)
        hc_time = (time.perf_counter() - start_hc) * 1000
        
        bt_solver = BacktrackingBinPacking(cap)
        start_bt = time.perf_counter()
        bt_sol, _ = bt_solver.optimize(items)
        bt_time = (time.perf_counter() - start_bt) * 1000
        
        results.append(
            BatchCompareItemResult(
                test_case_name=tc["name"],
                items_count=len(items),
                capacity=cap,
                hc=TestCaseResult(algorithm="Hill Climbing", num_bins=len(hc_sol.bins), time_ms=hc_time),
                bt=TestCaseResult(algorithm="Backtracking", num_bins=len(bt_sol.bins), time_ms=bt_time)
            )
        )
        
    return BatchCompareResponse(results=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
