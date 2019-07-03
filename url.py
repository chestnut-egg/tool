import os
import time

from flask import *
import logging
import configparser
from face.face import add_face


app = Flask(__name__)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cp = configparser.ConfigParser()
cp.read('myconfig.conf')

@app.route('/')
def hello_world():
    return redirect(url_for('idcard'))

@app.route('/hello')
def hello():
    return 'hello'

@app.route('/idcard')
def idcard():
    if request.method == 'GET':
        idnum = request.args.get('idnum')

        istrue = ''
        check = ''

        if(idnum != None):
            logger.info('idcard: %s',idnum)

            if idistrue(idnum) == 0:
                istrue="false"
            else:
                istrue="true"

        idnum2 = request.args.get('idnum2')
        if(idnum2 != None):

            if(len(idnum2) != 17):
                check = '不足17位'
            else:
                check = returncheck(idnum2)

        return render_template('idcard.html', check=check, istrue=istrue)

    istrue = ''
    check = ''
    return render_template('idcard.html', check=check, istrue=istrue)


def returncheck(idnum):
    tup = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    num = 0

    for i in range(0, 17):
        num += tup[i] * int(str(idnum)[i])
    logger.info('idcard-num: %d', num)
    yu = num % 11

    tup2 = (1, 0, -1, 9, 8, 7, 6, 5, 4, 3, 2)

    if tup2[yu] == -1:
        check = 'X'
    else:
        check = str(tup2[yu])

    logger.info('idcard-check: %s', check)
    return check


def idistrue(idnum):
    if len(idnum) != 18:
        logger.error('id != 18')
        return 0

    check = returncheck(idnum)

    if( (idnum[17] == 'X' or idnum[17] == 'x') and check == 'X'):
        logger.info('idcard-result: true')
        return 1

    if(idnum[17] == check):
        logger.info('idcard-result: true')
        return 1

    logger.info('idcard-result: false')
    return 0

@app.route('/face', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f1 = request.files['file1']
        f2 = request.files['file2']
        upload_address = cp.get('file','upload_address')

        t = str(int(time.time()))

        filename1 = t + "-1"
        filename2 = t + "-2"
        filename3 = t + "-3"

        file1 = upload_address + filename1
        file2 = upload_address + filename2

        f1.save(file1)
        f2.save(file2)
        result = 'success'

        file3 = upload_address + filename3

        add_face(file1,file2,file3,50)

        image_url = file3

        return render_template('face.html', result=result ,image_url = image_url)

    result = ''
    return render_template('face.html', result=result)


@app.route('/numtobig', methods=['GET', 'POST'])
def numtobig():
    if request.method == 'GET':
        num = request.args.get('num')

        if num == None:
            big = ''
            return render_template('numtobig.html', big=big, num = '')

        #零壹亿贰仟叁佰肆拾伍万陆仟柒佰捌拾玖
        tup1 = ('零','壹','贰','叁','肆','伍','陆','柒','捌','玖')
        tup2 = ('拾', '佰', '仟', '万', '亿')

        big = ''

        for i in range(0,len(str(num))):

            big += str(tup1[ int(str(num)[i]) ])

        return render_template('numtobig.html', big=big, num=num)

    big = ''
    return render_template('numtobig.html', big=big, num='')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')