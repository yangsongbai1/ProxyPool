import time
from multiprocessing import Process
from spider.verifier import Verifier
from spider.getter import Getter
from spider.setting import *
from spider.api import app

class Scheduler:
    '''调度器'''

    def scheduler_verify(self,cycle=VERIFY_CYCLE):
        '''
        启动验证器
        VERIFY_CYCLE    验证周期
        '''
        time.sleep(3)
        verifier = Verifier()
        while True:
            verifier.run_verify()
            time.sleep(cycle)

    def scheduler_getter(self,cycle=GET_CYCLE):
        '''
        启动获取器
        GET_CYCLE   获取周期
        '''
        getter = Getter()
        while True:
            getter.run_getter()
            time.sleep(cycle)

    def scheduler_api(self):
        app.run(API_HOST,API_PORT)

    def run(self):
        if VERIFY_ENABLED:
            verify_process = Process(target=self.scheduler_verify)
            verify_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()

if __name__ == '__main__':
    a = Scheduler()
    a.run()