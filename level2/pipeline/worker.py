




import redis
from rq import Queue, Connection
from ..dto import AnalysisConfig
from ..repository.weaviate_repo import WeaviateRepository
from ..pipeline.orchestrator import Level2Orchestrator
import os

def run_analysis(project_id: str, cfg_dict: dict):
    # Mock client for testing - replace with actual Weaviate client in production
    client = None
    repo = WeaviateRepository(client)
    orch = Level2Orchestrator(repo)
    cfg = AnalysisConfig(**cfg_dict)
    return orch.analyze_project(project_id, cfg).model_dump()

def main():
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    conn = redis.from_url(redis_url)
    with Connection(conn):
        q = Queue("level2")
        # rq worker запускается отдельно: rq worker level2
        # задачи кидаем через API (см. выше)

if __name__ == "__main__":
    main()




