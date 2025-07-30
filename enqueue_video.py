




import argparse
from rq import Queue
import redis
from tasks import process_video_task

# Try to use a real Redis server, fall back to fakeredis for testing
try:
    redis_url = "redis://localhost:6379"
    conn = redis.from_url(redis_url)
    # Test the connection
    conn.ping()
except (redis.ConnectionError, redis.AuthenticationError):
    print("[WARNING] Could not connect to Redis server, using fakeredis for testing")
    from fakeredis import FakeStrictRedis
    conn = FakeStrictRedis()

q = Queue(connection=conn)

def main():
    parser = argparse.ArgumentParser(description="Добавить видео в очередь обработки")
    parser.add_argument("video_path", type=str)
    parser.add_argument("--source", type=str, default="user_upload")
    args = parser.parse_args()

    job = q.enqueue(process_video_task, args.video_path, args.source)
    print(f"[INFO] Задание добавлено в очередь. Job ID: {job.id}")

if __name__ == "__main__":
    main()



