#!/app/venv/python
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/app/')
from davsrv import app as application
application.secret_key = 'changeme'
