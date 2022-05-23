from gocqhttpbot.botstart import RunThread
import os
from gocqhttpbot.botstart.util import init
import threading
if __name__ == '__main__':

    os.system(r'taskkill /F /IM go-cqhttp_windows_386.exe')
    try:
        # threading.Thread(target=RunThread.run ,args=()).start()
        RunThread.runapp().start()
        RunThread.runexe().start()
        RunThread.runhire().start()
        RunThread.runsky().start()
        RunThread.del_msg_monitor().start()
        threading.Thread(init.get_config()).start()
    except Exception as ee:
        print("入口出错%s" % ee)