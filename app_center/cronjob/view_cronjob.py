from pytz import timezone
from app_center.cronjob import  controller_cronjob

JAKARTA = timezone('Asia/Jakarta')

# # -------------- Daftar job ---------------------
# # def job_nt_mesin(scheduler):
# #   scheduler.add_job(
# #     func=controller_cronjob.run_nt_mesin,
# #     id='nt_patri_mesin',
# #     trigger='cron',
# #     day_of_week='mon-sun',
# #     hour=23,
# #     minute=59,
# #     timezone=JAKARTA,
# #     max_instances=1,
# #     coalesce=True,
# #     misfire_grace_time=3600,
# #     replace_existing=True
# #   )
# #   print("--CRONJOB NT-MESIN TERDAFTAR--")

# # def job_get_analisa_dt(scheduler):
# #   scheduler.add_job(
# #     func=controller_cronjob.run_get_analisa_dt,
# #     id='job_analisa_dt',
# #     trigger='interval',
# #     minutes=10,
# #     max_instances=1,
# #     coalesce=True,
# #     misfire_grace_time=3600,
# #     replace_existing=True
# #   )
# #   print("--CRONJOB ANALISA DT TERDAFTAR--")
  
# # -------------- Memanggil job (berasal dari init) ---------------------
def register_all_jobs(scheduler):
  # job_nt_mesin(scheduler)
  # job_get_analisa_dt(scheduler)
  print("CRONJOB REGISTER")