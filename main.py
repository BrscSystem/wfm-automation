import threading

from app.automation import automation
from app.trail import run as run_trail

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=automation.start_scheduler)
    scheduler_thread.start()

    trail_thread = threading.Thread(target=run_trail)
    trail_thread.start()

    scheduler_thread.join()
    trail_thread.join()
