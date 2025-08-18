




import pytest
from httpx import AsyncClient
from main import app # assuming the main FastAPI app is named app

@pytest.mark.asyncio
async def test_vote_flow(async_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 1. submit a vote
        resp = await ac.post("/teamwork/vote", json={
            "project_id": "p1",
            "task_id": "t1",
            "votes": [{"voter_id": "u1", "value": "yes"}],
            "vote_scheme": "binary"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["decision"] in ("approve","reject","no_consensus")

        # 2. load UI form
        resp_form = await ac.get("/ui/teamwork/vote")
        assert resp_form.status_code == 200
        assert "Голосование" in resp_form.text

        # 3. simulate form submission
        resp_submit = await ac.post("/ui/teamwork/vote", data={
            "project_id": "p1",
            "task_id": "t1",
            "voter_id": "u2",
            "value": "no"
        })
        assert resp_submit.status_code == 200
        assert "Результаты голосования" in resp_submit.text




