from gocqhttpbot.botstart import RunThread
import os


if __name__ == '__main__':

    os.system(r'taskkill /F /IM go-cqhttp_windows_386.exe')
    try:
        RunThread.runapp().start()
        RunThread.runexe().start()
        RunThread.runhire().start()
        RunThread.runsky().start()
    except:
        pass





