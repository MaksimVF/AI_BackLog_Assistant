





import pytest
from httpx import AsyncClient
from main import app # your FastAPI app
from level2.db.repo_teamwork import TeamworkRepo

@pytest.mark.asyncio
async def test_heatmap_endpoint(async_session):
    # preparation: create a couple of votes through repository or API
    repo = TeamworkRepo(async_session)
    # Save some records manually (use ORM/repository)
    await repo.save_voting("proj_heat", "task1", [{"voter_id":"u1","value":"yes","weight":1}], {"decision":"approve"})
    await repo.save_voting("proj_heat", "task2", [{"voter_id":"u2","value":"no","weight":1}], {"decision":"reject"})

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/ui/teamwork/heatmap/proj_heat")
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("image/png")
        assert len(resp.content) > 0





