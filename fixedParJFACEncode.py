import subprocess
proc = subprocess.Popen(['dir'], \
        stdin=subprocess.PIPE, \
        stdout=subprocess.PIPE)
print("Hello world")
