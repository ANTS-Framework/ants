"""logger
================

Handle logging.
"""


import os
import sys
import logging
import logging.handlers

from antslib import configer


CFG = configer.read_config('main')
logfile_main = os.path.join(CFG['log_dir'], 'ants.log')
logfile_ok = os.path.join(CFG['log_dir'], 'ok.log')
logfile_changed = os.path.join(CFG['log_dir'], 'changed.log')
logfile_failed = os.path.join(CFG['log_dir'], 'failed.log')
logfile_recap = os.path.join(CFG['log_dir'], 'recap.log')


def get_logger(name, logfile=False, maxBytes=0, formatter='default'):
    """Return logging object with handler and formatter."""
    if logfile:
        handler = logging.handlers.RotatingFileHandler(logfile,
                                                       maxBytes=maxBytes,
                                                       backupCount=5,
                                                       delay=True)
        handler.setLevel(logging.INFO)
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

    if formatter is 'default':
        handler.setFormatter(logging.Formatter('%(asctime)s\t%(message)s',
                                               datefmt='%b %d %Y %H:%M:%S %Z'))
    elif formatter is 'simple':
        handler.setFormatter(logging.Formatter('%(message)s'))
    else:
        raise ValueError('Formatter must be simple or default')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def status_file_rollover():
    """Rotate log files at the start of every ansible run


    Keep track of ok/changed/failed on a per run basis.
    Hence, rotate them at the start of each run.

    Code for rotation based on
    https://stackoverflow.com/questions/4654915/rotate-logfiles-each-time-the-application-is-started-python
    """
    if os.path.isdir(CFG['log_dir']):
        status_files = [[ok_logger, logfile_ok],
                        [changed_logger, logfile_changed],
                        [failed_logger, logfile_failed]]
        for (logger, logfile) in status_files:
            if os.path.isfile(logfile):
                console_logger.debug("Logfile rollover for file %s" % logfile)
                logger.handlers[0].doRollover()
    return


def log_recap(start_time, end_time, status_line):
    """Log play recap in a dedicated form.

    Rollover old logfiles befor writing.
    """
    if os.path.isfile(logfile_recap):
        console_logger.debug("Logfile rollover for file %s" % logfile_recap)
        recap_logger.handlers[0].doRollover()

    recap_logger.info('****PLAY TIME****')
    recap_logger.info('Start time: %s' % start_time)
    recap_logger.info('End time: %s' % end_time)
    recap_logger.info('Total: %s' % (end_time - start_time))
    recap_logger.info('****PLAY RECAP****')
    recap_logger.info(status_line.rstrip())
    recap_logger.info('Client status: %s' % parse_client_status(status_line))
    return


def parse_client_status(status_line):
    """Read client status from recap log.

    Status can have one of the following forms:
    * ok
    * changed
    * failed

    We expect IndexError because play recap will be
    empty if no matching hosts were found.
    Client status will be set to failed in that case.

    Status will also be set to failed of no log file
    could be found."""

    status = 'failed'
    try:
        status_list = status_line.split(':')[1].split()
        for f in status_list:
            g = f.split('=')
            if g[1] != '0':
                status = g[0]
    except IndexError:
        pass
    return status


def write_log(line, task_line=None, debug=False):
    """Write log to stdout and log files.


    Highlight ansible run status in stdout."""
    if not os.path.isdir(CFG['log_dir']):
        configer.create_dir(CFG['log_dir'])
    if line.startswith('ok:'):
        if task_line is not None:
            ok_logger.info(task_line.rstrip())
        console_logger.info("\033[0;32m%s\033[0;0m" % line.rstrip())
        ok_logger.info(line.rstrip())
    elif line.startswith('changed:'):
        if task_line is not None:
            changed_logger.info(task_line.rstrip())
        console_logger.info("\033[1;33m%s\033[0;0m" % line.rstrip())
        changed_logger.info(line.rstrip())
    elif line.startswith('failed:') or line.startswith('fatal:'):
        if task_line is not None:
            failed_logger.info(task_line.rstrip())
        console_logger.info("\033[0;31m%s\033[0;0m" % line.rstrip())
        failed_logger.info(line.rstrip())
    elif line.startswith('skipping:'):
        console_logger.info("\033[1;36m%s\033[0;0m" % line.rstrip())
    else:
        console_logger.info(line.rstrip())
    logfile_logger.info(line.rstrip())
    return


console_logger = get_logger("console_logger", formatter='simple')
logfile_logger = get_logger("logfile_logger", logfile_main, 5000000)
ok_logger = get_logger("ok_logger", logfile_ok)
changed_logger = get_logger("changed_logger", logfile_changed)
failed_logger = get_logger("failed_logger", logfile_failed)
recap_logger = get_logger("recap_logger", logfile_recap)

if __name__ == '__main__':
    pass
