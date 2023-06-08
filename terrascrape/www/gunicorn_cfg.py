import setproctitle


def post_worker_init(_):
    """
    Set process title.
    """
    setproctitle.setproctitle(f'[ready] {setproctitle.getproctitle()}')


bind = '0.0.0.0:5000'
accesslog = '-'
loglevel = 'debug'
capture_output = False
enable_stdio_inheritance = False
