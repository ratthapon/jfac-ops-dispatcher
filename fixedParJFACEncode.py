import subprocess

proc = subprocess.Popen(['mvn','test'], \
        stdin=subprocess.PIPE, \
        stdout=subprocess.PIPE, \
        shell=True, \
        bufsize=1, \
        universal_newlines=True, \
        cwd='..\\java-fractal-audio-compression')
for line in proc.stdout.read():
    print(line, end='')
    
stdout, stderr = proc.communicate()
proc.stdout.close()
