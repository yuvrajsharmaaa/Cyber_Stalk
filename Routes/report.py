from aquilify.wrappers import Request, Response
from aquilify import responses, shortcuts

async def cyberStalkingReportpage(request: Request) -> Response:
    return await shortcuts.render(request = request, template_name = "reporting.html")