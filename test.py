import os
import sys
import imp
import argparse
import traceback
from multiprocessing import Process
from dotenv import load_dotenv, find_dotenv

# collect args
parser = argparse.ArgumentParser()
parser.add_argument('--env_name',  help="conda env name")
args = parser.parse_args()

# create a new conda env
env_name = None
if args.env_name:
    env_name = args.env_name
else:
    env_name = '2023-10-24'
ENV_NAME = "NIS7024-homework-test-%s" % env_name
load_dotenv(find_dotenv(".env"), verbose=True)
PYTHON_VERSION = os.getenv('PYTHON_VERSION')
print("PYTHON VERSION collected:", PYTHON_VERSION)
print("Preparing create conda env...")

def check_and_exit(exit_code, ret_status):
    if exit_code != 0:
        exit(ret_status)
exit_code = os.system("conda remove -n %s --all -y" % ENV_NAME)
check_and_exit(exit_code, 1)
exit_code = os.system("conda create -n %s python=%s -y" % (ENV_NAME, PYTHON_VERSION))
check_and_exit(exit_code, 2)
print("conda env created.")

# install python packages
exit_code = os.system("pip install -r requirements.txt")
check_and_exit(exit_code, 3)
print("python packages installed.")

# load train & Parameters
def get_params_from_file(filename, path):
    file, pathname, description = imp.find_module(filename, path=[path])
    mod = imp.load_module('generated_str', file, pathname, description)
    return mod.train, mod.Parameters

train, Parameters = get_params_from_file(filename='main', path="./code")
# test the train & Parameters
try:
    params = Parameters()
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None)
    exit(4)
try:
    params = Parameters()
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=open("./error_file_test.log", 'w+'))
    exit(5)
print("train & Parameters test passed.")
# setup the training task
print("setting up training process...")
PYTHON_DIR = os.popen("conda env list | grep %s" % ENV_NAME).read().split()[1] 
PYTHON_PATH = PYTHON_DIR + "/bin/python3"
print("Got PYTHON_PATH:", PYTHON_PATH)
def task_wrapper(name, status):
    try:
        exit_code = os.system("%s ./code/main.py" % name)
        check_and_exit(exit_code, 6)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None)
        exit(7)
p = Process(target=task_wrapper, args=(ENV_NAME, 6))
p.start()
p.join()
# delete conda env
exit_code = os.system("conda remove -n %s --all -y" % ENV_NAME)
check_and_exit(exit_code, -1)
print("test done!")