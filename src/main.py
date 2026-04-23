import asyncio
import uvicorn

from app import create_app
from core.config import settings

# создаём приложение
app = create_app()


# описывает как запустить приложение
async def run() -> None:
    config = uvicorn.Config("main:app", host="localhost", port=settings.PORT, reload=False)
    server = uvicorn.Server(config=config) # создаём сервер по конфигу

    # предоставляем задачи через кортеж
    tasks = (
        asyncio.create_task(server.serve()),
    )

    # пока не выполнится хотя бы первая задача
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

# точка входа в программу
if __name__ == "__main__":

    # запускаем цикл ивентов пока не выполнится
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
