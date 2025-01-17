from sqlalchemy import (
    create_engine,
)
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette_admin.contrib.sqla import Admin

from .config import ENGINE_URI
from .models import Base, Post, User
from .views import PostView, UserView

engine = create_engine(ENGINE_URI, connect_args={"check_same_thread": False}, echo=True)


def init_database() -> None:
    Base.metadata.create_all(engine)


app = Starlette(
    routes=[
        Route(
            "/",
            lambda r: HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>'),
        )
    ],
    on_startup=[init_database],
)

# Create admin
admin = Admin(
    engine,
    title="SQLA + Pydantic",
)

# Add views
admin.add_view(UserView(User, icon="fa fa-users"))
admin.add_view(PostView(Post, icon="fa fa-blog", label="Blog Posts"))

# Mount admin
admin.mount_to(app)
