from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime, timedelta
from pytz import timezone
import os

def init_scheduler(app, db_url: str):
    scheduler = BackgroundScheduler(
        timezone=timezone('Asia/Jakarta'),
        jobstores={
            'default': SQLAlchemyJobStore(
                url=db_url,
                tablename='apscheduler_jobs'
            )
        }
    )

    # -------------- Listener untuk Sukses / Error ---------------------
    def job_listener(event):
        if event.exception:
            print(f"[ERROR] CRONJOB '{event.job_id}' GAGAL => {event.exception}")
            failed_job = scheduler.get_job(event.job_id)

            # Coba ulang dalam 1 menit jika belum pernah di-retry
            if failed_job and '_retry' not in event.job_id:
                retry_id = f"{event.job_id}_retry"
                print(f"[RETRY] {retry_id} dijadwalkan dalam 1 MENIT...")
                scheduler.add_job(
                    func=failed_job.func,
                    args=failed_job.args,
                    kwargs=failed_job.kwargs,
                    id=retry_id,
                    trigger='date',
                    run_date=datetime.now() + timedelta(minutes=1),
                    replace_existing=True
                )
        else:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{ts}] CRONJOB '{event.job_id}' SELESAI - Return: {event.retval}")

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    # -------------- Daftar dan Register Job ---------------------
    from .view_cronjob import register_all_jobs

    # with app.app_context():
    #     register_all_jobs(scheduler)
    env = os.environ.get('FLASK_ENV')
    with app.app_context():
        if env == 'Production':
            print("[INFO] Menjalankan cronjob di Production.")
            register_all_jobs(scheduler)
            scheduler.start()
        elif env == 'development':
            print("[INFO] Mode development - cronjob tidak dijalankan.")
        else:
            print(f"[WARNING] FLASK_ENV tidak dikenali: {env}")


    
