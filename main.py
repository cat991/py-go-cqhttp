from gocqhttpbot.botstart import RunThread
import os


if __name__ == '__main__':

    os.system(r'taskkill /F /IM go-cqhttp_windows_386.exe')
    try:
        thread1 = RunThread.runapp()
        thread1.start()
        thread2 = RunThread.runexe()
        thread2.start()
        thread3 = RunThread.runhire()
        thread3.start()
        thread4 = RunThread.runsky()
        thread4.start()
    except:
        pass





