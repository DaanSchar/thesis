from typing import Protocol

from .result import PipelineResult


class AsyncDataPipeline(Protocol):
	async def run(self) -> PipelineResult: ...
