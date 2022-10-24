import asyncio
import time

# asyncio 예제
# delay 파라미터에 각 1초 2초를 넣어 실행하였으나 2초밖에 걸리지 않음
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def asyncio_main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")

asyncio.run(asyncio_main())


# 같은 방식을 기본적으로 구현하면 3초가 걸린다.
def say_after(delay, what):
    time.sleep(delay)
    print(what)

def main():
    print(f"started at {time.strftime('%X')}")
    say_after(1, 'hello')
    say_after(2, 'world')
    print(f"finished at {time.strftime('%X')}")

main()