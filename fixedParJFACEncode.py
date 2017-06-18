import subprocess
from itertools import product
'''
Dispatch the cmd to exec the java-fractacl-audio-compression by maven with 
default parameters.
'''
def dispatch(args):
    paramsFilePath = "'..\\settings\\default-params.txt'";
    mvnWorkingDir = '..\\java-fractal-audio-compression';
#    batchCMD = ['mvn','exec:exec','-Dparams=' + paramsFilePath ];
    batchCMD = ['mvn','exec:exec' ];
    
    params = open('..\\settings\\default-params.txt', 'r');
    
    # set process
    process = subprocess.Popen(batchCMD, \
                stdin = subprocess.PIPE, \
                stdout = subprocess.PIPE, \
                shell = True, \
                bufsize = 8, \
                universal_newlines = True, \
                cwd = mvnWorkingDir)
    
    process.stdin.write(args)
    
#    # notify build msgs
    for line in iter(process.stdout.readline, ""):
        print(line, end='')
        
    # free I/O
    process.stdout.close()
    
'''
Buil the parameters for batch JFAC processing.
'''
def buildParamsStr():
    FS = ['8', '16']
    RBS = ['128','64']
    COEFF = ['1.4', '1.3']
    
    PARAMS = list(product(FS, RBS, COEFF))
    PARAMSSCRIPT = []
    
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
        PARAMSSCRIPT += ['\n'.join(paramsScript) + '\n\n']
    
    return PARAMSSCRIPT

PS = buildParamsStr()
print( PS[0] )
dispatch( PS[0] )






