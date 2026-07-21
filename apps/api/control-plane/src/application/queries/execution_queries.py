from dataclasses import dataclass

from src.application.dto import Query


@dataclass(frozen=True)
class GetExecutionQuery(Query):
    execution_id: str
