from vintran import app, scheduler
from vintran.tasks import check_expired_files

if __name__ == "__main__":
    scheduler.add_job(
        id="check_expired_files",
        func=check_expired_files,
        trigger="interval",
        seconds=60,
    )
    scheduler.start()
    app.run(debug=True, use_reloader=False)
