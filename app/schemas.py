from pydantic import BaseModel
from typing import List, Optional

class OptimizationRequest(BaseModel):
    items: List[int]
    capacity: int
    algorithm: str  # "hc"
    max_iter: Optional[int] = 500
    verify_optimal: Optional[bool] = False

class BinResponse(BaseModel):
    items: List[int]
    used: int
    capacity: int

class OptimizationResult(BaseModel):
    algorithm: str
    bins: List[BinResponse]
    history: List[float]
    num_bins: int
    optimal_bins: Optional[int] = None
    time_ms: Optional[float] = None

class BatchCompareRequest(BaseModel):
    batch_text: str

class TestCaseResult(BaseModel):
    algorithm: str
    num_bins: int
    time_ms: float

class BatchCompareItemResult(BaseModel):
    test_case_name: str
    items_count: int
    capacity: int
    hc: TestCaseResult
    bt: TestCaseResult

class BatchCompareResponse(BaseModel):
    results: List[BatchCompareItemResult]
