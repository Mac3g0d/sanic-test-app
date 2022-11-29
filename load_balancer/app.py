from sanic import Sanic, response, HTTPResponse, Request
from sqlalchemy import select

from .services.transform_cdn_url import TransformCdnUrlService
from .config import LoadBalancerConfig
from .models import CDNHost
from .utils import startup, inject_session, close_session

app = Sanic(name='load_balancer_app')
app.config.update_config(LoadBalancerConfig)

app.register_listener(startup, 'before_server_start')

app.register_middleware(inject_session, 'request')
app.register_middleware(close_session, 'response')


@app.route("/")
async def balance_load(request: Request) -> HTTPResponse:
    video_url = request.args.get('video', None)
    print(app.config['REQUESTS_COUNT'])
    if video_url:
        if app.config['REQUESTS_COUNT'] >= app.config['REDIRECT_REQUEST_NUM']:
            app.config['REQUESTS_COUNT'] = 0

            return response.text(video_url)

        cnd_hosted_url = await TransformCdnUrlService(video_url, request.ctx.session)()
        app.config['REQUESTS_COUNT'] += 1

        return response.text(cnd_hosted_url)

    return response.text('query parameter `video` is required', status=400)


@app.route("/health")
async def healthcheck(request: Request) -> HTTPResponse:

    qq = await request.ctx.session.execute(select(CDNHost))
    return response.text(f'{list(qq)}')

