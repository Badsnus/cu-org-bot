from .show_tasks import router as show_tasks_router
from .solve_tasks import router as solve_tasks_router
from .start import router as start_router
from .team import router as team_router

routers = [
    start_router,
    show_tasks_router,
    solve_tasks_router,
    team_router,
]
