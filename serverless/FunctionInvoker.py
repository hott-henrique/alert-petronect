import typing as t

from celery import current_app


class FunctionInvoker:

    def __init__(self) -> None:
        self.app = current_app

    def trigger(self, name: str, event: dict, delayed: t.Optional[float] = None):
        task = self.app.tasks.get(name)  # type: ignore

        if task is None:
            raise ValueError(f"Task '{name}' not found.")

        task.apply_async(args=[ event, dict() ], countdown=delayed)
