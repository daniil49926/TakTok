from views import main_page


def setup_routes(app) -> None:
    app.router.add_get("/", main_page)
