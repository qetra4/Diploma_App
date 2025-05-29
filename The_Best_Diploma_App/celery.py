from celery import Celery
from The_Best_Diploma_App import settings 
from dotenv import load_dotenv

load_dotenv()
app = Celery('The_Best_Diploma_App')
app.config_from_object('The_Best_Diploma_App.settings', namespace='CELERY')
app.autodiscover_tasks(['The_Best_Diploma_App'])
app.conf.worker_state_db = settings.CELERY_WORKER_STATE_DB 
