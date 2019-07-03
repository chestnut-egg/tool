import os
import time
from flask import *
import logging
import configparser

app = Flask(__name__)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cp = configparser.ConfigParser()
cp.read('myconfig.conf')



@app.route('/os')
def oss():
    ps = os.popen('ps -ef')
    list = []
    for temp in ps.readlines():
        logger.info(temp)
        list.append(temp)
    info={}
    info['pslist'] = list
    return render_template('os.html', info = info)




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')