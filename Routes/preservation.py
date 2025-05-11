from aquilify.wrappers import Request, Response
from aquilify import responses, shortcuts

async def cyberStalkingPreservationpage(request: Request) -> Response:
    return await shortcuts.render(request = request, template_name = "preservation.html")