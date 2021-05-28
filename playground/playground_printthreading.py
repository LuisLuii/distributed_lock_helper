import asyncio
import requests
import queue

class TaskGenerator():
    def __init__(self):
        self.queue = queue.Queue(10)

    def append_task(self, ):
        pass

async def get_data(task_id):
  #print("start get data from", task_id)
  await asyncio.sleep(3)
  # for i in range(5000000):
  #   pass
  #print("get success ", task_id)

async def get_and_send_data(task_id):
  await get_data(task_id)
  #print("send get data from", task_id)
  requests.get('http://127.0.0.1:5000/')
  #print("send success ", task_id)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*[get_and_send_data(i) for i in range(10)]))