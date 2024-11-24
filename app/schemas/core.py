from enum import Enum
from pydantic import BaseModel

class GraphType(Enum):
    LINE = "line"
    HORIZONTAL_LINE = "horizontal_line"
    STACKED_LINE = "stacked_line"
    BAR = "bar"
    STACKED_BAR = "stacked_bar"
    HORIZONTAL_BAR = "horizontal_bar"
    PIE = "pie"
    DONUT = "donut"

class PreliminaryAnalyseResponse(BaseModel):
    domain: str
    columns: list[str]
    def to_dict(self):
        return self.model_dump()

class GenerateQuestionsResponse(BaseModel):
    questions: list[str]
    def to_dict(self):
        return self.model_dump()

class PickGraphTypeResponse(BaseModel):
    graph_type: GraphType
    reason: str
    def to_dict(self):
        return self.model_dump()

class GenerateCodeResponse(BaseModel):
    code: str
    def to_dict(self):
        return self.model_dump()