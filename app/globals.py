import os 

scriptDir = os.path.dirname(os.path.realpath(__file__))

dataPath = '/tmp'
if os.getenv('src') != None:
    if os.path.isdir(os.getenv('src')):
        dataPath = os.getenv('src')

tmpPath = '/tmp'