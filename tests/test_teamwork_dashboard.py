





import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_dashboard_view(async_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create a voting record
        await ac.post("/teamwork/vote", json={
            "project_id": "p1",
            "task_id": "t2",
            "votes": [{"voter_id": "u1", "value": "yes"}],
            "vote_scheme": "binary"
        })

        # check dashboard
        resp = await ac.get("/ui/teamwork/dashboard/p1")
        assert resp.status_code == 200
        assert "Результаты голосований" in resp.text
        assert "u1 → yes" in resp.text





