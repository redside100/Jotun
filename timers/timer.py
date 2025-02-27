import asyncio
import threading


# Fucking black magic (threaded asyncio coroutines)
class Timer:

    # The force argument is only used to notify end/event functions that it's been force called by a timer
    def __init__(self, seconds, event_loop, end_func, *args, force=False):
        self.current_tick = seconds
        self.end_func = end_func
        self.event_func = None
        self.event_args = None
        self.event_tick = None
        self.args = args
        self.force = force
        self.alive = True
        self.cancelled = False
        # We gotta use the main asyncio event loop to interact with the bot
        self.main_event_loop = event_loop

    async def callback(self):
        await self.start_timer()

    def between_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.callback())
        loop.close()

    def start(self):
        thread = threading.Thread(target=self.between_callback)
        thread.start()

    # Start the timer
    async def start_timer(self):
        # Tick
        while self.current_tick > 0 and not self.cancelled:
            await asyncio.sleep(1)
            self.current_tick -= 1
            # Check for event
            if self.event_tick == self.current_tick:
                # Call event coroutine if exists
                if all(var is not None for var in [self.event_func, self.event_args, self.event_tick]):
                    # No weird delay when using this function
                    if self.force:
                        asyncio.run_coroutine_threadsafe(self.event_func(*self.event_args, force=self.force),
                                                         self.main_event_loop)
                    else:
                        asyncio.run_coroutine_threadsafe(self.event_func(*self.event_args), self.main_event_loop)

        if not self.cancelled:
            # No longer alive, call end coroutine
            self.alive = False
            if self.force:
                asyncio.run_coroutine_threadsafe(self.end_func(*self.args, force=self.force), self.main_event_loop)
            else:
                asyncio.run_coroutine_threadsafe(self.end_func(*self.args), self.main_event_loop)

    def set_event(self, time, func, *args):
        self.event_func = func
        self.event_args = args
        self.event_tick = time

    def get_time_left(self):
        return self.current_tick

    def cancel(self):
        self.cancelled = True

