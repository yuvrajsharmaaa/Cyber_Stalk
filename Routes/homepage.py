from aquilify.wrappers import Request, Response
from aquilify import responses, shortcuts

async def cyberStalkingHomepage(request: Request) -> Response:
    return await shortcuts.render(request = request, template_name = "index.html")