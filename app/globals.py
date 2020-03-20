import os 

scriptDir = os.path.dirname(os.path.realpath(__file__))

tmpPath = '/tmp'

urlBase = ''
if os.getenv('base') != None:
    urlBase = os.getenv('base')

dataPath = '/home'
if os.getenv('src') != None:
    if os.path.isdir(os.getenv('src')):
        dataPath = os.getenv('src')

