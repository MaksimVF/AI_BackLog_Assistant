



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
import io
import matplotlib
matplotlib.use("Agg") # for rendering in server environment without GUI
import matplotlib.pyplot as plt

from ...db.repo_teamwork import TeamworkRepo
from ...db.session import get_async_session

router = APIRouter(prefix="/ui/teamwork", tags=["Teamwork-UI"])

@router.get("/heatmap/{project_id}")
async def heatmap(project_id: str, session: AsyncSession = Depends(get_async_session)):
    repo = TeamworkRepo(session)
    task_ids, voter_ids, matrix = await repo.build_votes_matrix(project_id, latest_only=True)

    if not task_ids or not voter_ids:
        raise HTTPException(status_code=404, detail="No voting data for project")

    # Build matrix (matplotlib)
    fig, ax = plt.subplots(figsize=(max(6, len(voter_ids)*0.4), max(4, len(task_ids)*0.4)))
    cax = ax.imshow(matrix, aspect='auto')  # don't specify cmap explicitly
    # Labels
    ax.set_xticks(range(len(voter_ids)))
    ax.set_xticklabels(voter_ids, rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(len(task_ids)))
    ax.set_yticklabels(task_ids, fontsize=8)
    ax.set_title(f"Voting heatmap — project {project_id}")
    fig.colorbar(cax, ax=ax, orientation='vertical')

    # Tight layout
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")



