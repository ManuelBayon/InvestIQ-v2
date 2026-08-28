import asyncio
from asyncio import Future


def i_am_callback(fut: Future):
    print("I am the callback you waited for.")

def i_am_a_coroutine():
    print("I am a coroutine.")

if __name__ =="__main__":

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


    fut = loop.create_future()
    print("doing some things...")
    fut.set_result(True)
    fut.add_done_callback(i_am_callback)

    loop.run_until_complete(fut)
