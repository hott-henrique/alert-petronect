from celery import Celery

import os, sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

if __name__ == "__main__":
    app = Celery(broker="redis://localhost:6379/0")

    print(app.send_task("check_for_biddings", args=[dict(), dict()]))
