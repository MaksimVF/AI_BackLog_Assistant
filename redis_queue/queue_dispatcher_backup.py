







from rq import Queue
from redis import Redis

# Redis URL можно брать из переменной окружения
redis_conn = Redis(host='localhost', port=6379)
video_queue = Queue('video_processing', connection=redis_conn)
image_queue = Queue('image_processing', connection=redis_conn)
transcription_queue = Queue('transcription', connection=redis_conn)

def enqueue_video_task(video_path):
    from redis_queue.workers.video_worker import process_video_file
    video_queue.enqueue(process_video_file, video_path)

def enqueue_image_task(image_path):
    from redis_queue.workers.image_worker import process_image_file
    image_queue.enqueue(process_image_file, image_path)

def enqueue_transcription_task(audio_path):
    from redis_queue.workers.transcription_worker import transcribe_audio_file
    transcription_queue.enqueue(transcribe_audio_file, audio_path)







