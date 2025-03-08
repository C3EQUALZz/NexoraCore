from faststream import ContextRepo, FastStream
from dishka.integrations.faststream import setup_dishka
from app.logic.container import container
from app.settings.config import Settings
from app.application.message_handlers.broker import broker

app = FastStream(broker)


@app.on_startup
async def setup(context: ContextRepo):
    settings = await container.get(Settings)
    context.set_global("settings", settings)
    setup_dishka(app=app, container=container, auto_inject=True)
    await broker.connect(settings.broker.host)


@app.on_shutdown
async def cleanup():
    container.close()
