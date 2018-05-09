import time
import argparse
from subprocess import getoutput


def get_guilty_proc():
    "returns a PID for the process consuming high RAM at the time"
    cmd = "ps aux --sort rss| tail -n 1 | awk '{print $11, $2}'"
    out = getoutput(cmd)
    return out.strip().split()


def suspend_proc(pid):
    cmd = 'kill -STOP ' + pid
    getoutput(cmd)


def current_free():
    cmd = "free | grep Mem | awk '{print $4}'"
    return int(getoutput(cmd))


def notify(proc, pid):
    body = '''
    The process
    {proc}
    has been suspended due to low RAM.

    you can resume it by running

    kill -CONT {pid}

    or you can terminate it by running

    kill -KILL {pid}

    For Jupyter sending a interrupt usually works to stop the cell
    without stopping Jupyter.

    kill -INT {pid}
    '''.format(pid=pid, proc=proc)
    cmd = "notify-send -u critical Fukasaku '{body}'".format(body=body)
    getoutput(cmd)
    print(proc, pid, 'suspended')


def watch(interval, ram_limit):
    dealt_with = False
    while True:
        if (current_free() < ram_limit):
            if not dealt_with:
                proc, pid = get_guilty_proc()
                suspend_proc(pid)
                dealt_with = True
                notify(proc, pid)
        else:
            dealt_with = False
        time.sleep(interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='process suspender')
    parser.add_argument('-m', default='1G',
                        help='Start suspending when RAM is below this limit 1G, 500M')
    parser.add_argument('-i', default='2s',
                        help='At what interval to check for RAM usage. 2s, 1m')

    args = parser.parse_args()
    if args.i[-1] in 'sS':
        i = float(args.i[:-1])
    elif args.i[-1] in 'mM':
        i = float(args.i[:-1]) * 60
    else:
        raise Exception("Unknown time format. Please use s/m")

    if args.m[-1] in 'gG':
        m = float(args.m[:-1]) * 1024 * 1024
    elif args.m[-1] in 'mM':
        m = float(args.m[:-1]) * 1024
    else:
        raise Exception("Unknown time format. Please use g/m")

    watch(i, m)
