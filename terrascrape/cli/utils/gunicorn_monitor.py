import signal
import sys
import time
from typing import NoReturn

import psutil

from terrascrape.exceptions import WEBSERVER_ERROR_TIMEOUT, WebserverException


class GunicornMonitor:
    def __init__(
        self,
        gunicorn_master_pid: int,
        num_workers_expected: int
    ):
        super().__init__()
        self.gunicorn_master_proc = psutil.Process(gunicorn_master_pid)
        self.num_workers_expected = num_workers_expected
        self.master_timeout = 120
        self.worker_refresh_interval = 6000
        self.worker_refresh_batch_size = 1

        self._num_workers_running = 0
        self._num_ready_workers_running = 0
        self._last_refresh_time = time.monotonic() if self.worker_refresh_interval > 0 else None
        self._restart_on_next_plugin_check = False

    def _get_num_ready_workers_running(self) -> int:
        """Returns number of ready Gunicorn workers by looking for READY_PREFIX in process name"""
        workers = psutil.Process(self.gunicorn_master_proc.pid).children()

        def ready_prefix_on_cmdline(proc):
            try:
                cmdline = proc.cmdline()
                if len(cmdline) > 0:
                    return '[ready] ' in cmdline[0]
            except psutil.NoSuchProcess:
                pass
            return False

        ready_workers = [proc for proc in workers if ready_prefix_on_cmdline(proc)]
        return len(ready_workers)

    def _get_num_workers_running(self) -> int:
        """Returns number of running Gunicorn workers processes"""
        workers = psutil.Process(self.gunicorn_master_proc.pid).children()
        return len(workers)

    def _wait_until_true(self, fn, timeout: int = 0) -> None:
        """Sleeps until fn is true"""
        start_time = time.monotonic()
        while not fn():
            if 0 < timeout <= time.monotonic() - start_time:
                raise WebserverException(WEBSERVER_ERROR_TIMEOUT)
            time.sleep(0.1)

    def _spawn_new_workers(self, count: int) -> None:
        """
        Send signal to kill the worker.
        :param count: The number of workers to spawn
        """
        excess = 0
        for _ in range(count):
            self.gunicorn_master_proc.send_signal(signal.SIGTTIN)
            excess += 1
            self._wait_until_true(
                lambda: self.num_workers_expected + excess == self._get_num_workers_running(),
                timeout=self.master_timeout,
            )

    def _kill_old_workers(self, count: int) -> None:
        """
        Send signal to kill the worker.
        :param count: The number of workers to kill
        """
        for _ in range(count):
            count -= 1
            self.gunicorn_master_proc.send_signal(signal.SIGTTOU)
            self._wait_until_true(
                lambda: self.num_workers_expected + count == self._get_num_workers_running(),
                timeout=self.master_timeout,
            )

    def _reload_gunicorn(self) -> None:
        """
        Send signal to reload the gunicorn configuration. When gunicorn receive signals, it reload the
        configuration, start the new worker processes with a new configuration and gracefully
        shutdown older workers.
        """
        self.gunicorn_master_proc.send_signal(signal.SIGHUP)
        time.sleep(1)
        self._wait_until_true(
            lambda: self.num_workers_expected == self._get_num_workers_running(), timeout=self.master_timeout
        )

    def start(self) -> NoReturn:
        """Starts monitoring the webserver."""
        try:
            self._wait_until_true(
                lambda: self.num_workers_expected == self._get_num_workers_running(),
                timeout=self.master_timeout,
            )
            while True:
                if not self.gunicorn_master_proc.is_running():
                    sys.exit(1)
                self._check_workers()
                time.sleep(1)

        except (OSError, Exception):
            try:
                self.gunicorn_master_proc.terminate()
                self.gunicorn_master_proc.wait()
            finally:
                sys.exit(1)

    def _check_workers(self) -> None:
        num_workers_running = self._get_num_workers_running()
        num_ready_workers_running = self._get_num_ready_workers_running()

        # Whenever some workers are not ready, wait until all workers are ready
        if num_ready_workers_running < num_workers_running:
            time.sleep(1)
            return

        # If there are too many workers, then kill a worker gracefully by asking gunicorn to reduce
        # number of workers
        if num_workers_running > self.num_workers_expected:
            excess = min(num_workers_running - self.num_workers_expected, self.worker_refresh_batch_size)
            self._kill_old_workers(excess)
            return

        # If there are too few workers, start a new worker by asking gunicorn
        # to increase number of workers
        if num_workers_running < self.num_workers_expected:
            time.sleep(10)
            num_workers_running = self._get_num_workers_running()
            if num_workers_running < self.num_workers_expected:
                new_worker_count = min(
                    self.num_workers_expected - num_workers_running, self.worker_refresh_batch_size
                )
                self._spawn_new_workers(new_worker_count)
            return

        # Now the number of running and expected worker should be equal

        # If workers should be restarted periodically.
        if self.worker_refresh_interval > 0 and self._last_refresh_time:
            # and we refreshed the workers a long time ago, refresh the workers
            last_refresh_diff = time.monotonic() - self._last_refresh_time
            if self.worker_refresh_interval < last_refresh_diff:
                num_new_workers = self.worker_refresh_batch_size
                self._spawn_new_workers(num_new_workers)
                self._last_refresh_time = time.monotonic()
                return
