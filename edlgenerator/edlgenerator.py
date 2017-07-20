#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "chevtsov"
__date__ = "$Feb 16, 2010 3:19:51 PM$"

from epics.ca import ChannelAccessException
import epics.pv
import os
import subprocess
import time

MAX_NR_READ_PV_TRIES = 10
def read_pvs(pvs):
    vals = []
    for pv in pvs:
        try_count = 0
        while True:
            if try_count >= MAX_NR_READ_PV_TRIES:
                return []
            try:
                val = epics.PV(pv).get()
                if val is None or val == []:
                    raise ChannelAccessException('', '')
                break
            except ChannelAccessException:
                print "%s not found. Trying again..." % pv
                try_count += 1
        vals.append(val)
    return vals

def run_edm_server():
    edm_args = ['nohup', 'edm', '-server']
    subprocess.Popen(edm_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def use_server():
    #e.g. :0.0 or localhost:22.0
    tokens = os.environ.get("DISPLAY").split(':')
    return len(tokens[0]) == 0

def write_edl_instance(edl_template, edl_file_path):
    edl = str(edl_template)

    edl_file = open(edl_file_path, 'w')
    edl_file.write(edl)
    edl_file.close()

def display_edl_instance(edl_template, edl_file_path):
    write_edl_instance(edl_template, edl_file_path)

    if use_server():
        edm_args = [
            'edm',
            '-x',
            '-open',
            edl_file_path
            ]
        process = subprocess.Popen(edm_args)
        (stdoutdata, stderrdata) = process.communicate()
        if process.returncode == 100:
            print "Starting new EDM server..."
            run_edm_server()
            time.sleep(3)
            print "EDM server started"
            display_edl_instance(edl_template, edl_file_path)
    else:
        edm_args = [
            'edm',
            '-x',
            edl_file_path
            ]
        subprocess.Popen(edm_args)

#Test
if __name__ == "__main__":
    print read_pvs(['a', 'b'])
