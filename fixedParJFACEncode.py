import subprocess
from itertools import product
'''
Dispatch the cmd to exec the java-fractacl-audio-compression by maven with 
default parameters.
'''
def dispatch(args):
    mvnWorkingDir = '..\\java-fractal-audio-compression';
    batchCMD = ['mvn','exec:exec' ];
    
    # set process
    process = subprocess.Popen(batchCMD, \
                stdin = subprocess.PIPE,       # set parameter input stream \
                stdout = subprocess.PIPE,      # set console output stream \
                shell = True, \
                bufsize = 8, \
                universal_newlines = True, \
                cwd = mvnWorkingDir)             # set working directory of cmd
                               
    # inject parameters to JFAC
    process.stdin.write(args)
    
    # notify build msgs
    for line in iter(process.stdout.readline, ""):
        print(line, end='')
        
    # free I/O
    process.stdout.close()
    
'''
Buil the parameters for batch JFAC processing.
'''
def buildParamsStr():
    # define values for each paramter
    FS = ['8', '16']
    RBS = ['128','64']
    COEFF = ['1.4', '1.3']
    
    # combination paramters with cartetian product
    PARAMS = list(product(FS, RBS, COEFF))
    PARAMSSCRIPT = []
    
    # build paramters script for each combination
    for params in PARAMS:
        fs = params[0]
        rbs = params[1]
        coeff = params[2]
        testName = str('AN4' + fs + '_FP_RBS' + rbs  + '_COEFF' + coeff)
    
        paramsScript = ['processname compress', \
                      'testname ' + testName, \
                      'infile ..//settings//an4traintest_small.txt', \
                      'inpathprefix ..//corpus//audio//BASE' + fs + '//wav//', \
                      'outdir ..//codes//', \
                      'maxprocess 1', \
                      'inext raw', \
                      'outext mat', \
                      'pthresh 0', \
                      'reportrate 0', \
                      'gpu true', \
                      'coefflimit ' + coeff, \
                      'skipifexist false', \
                      'minr ' + rbs, \
                      'maxr ' + rbs]
        
        # join and split line with Python concat convention
        PARAMSSCRIPT += ['\n'.join(paramsScript) + '\n\n']
    
    return PARAMSSCRIPT

'''
Run batch JFAC
'''
# build all parameter scripts
PARAMSSCRIPT = buildParamsStr()

# iterate over parameter scripts
for param in PARAMSSCRIPT:
    
    # run X time fault tolerance
    # JCUDA maybe segfault during operation
    for faultTolerance in range(10):
        print("Trying no. " + str(faultTolerance)) # indicate tolerance iteration
        dispatch( param ) # exec each parameter script

