# _*_ coding: UTF-8 _*_
#导入拓展
from flask_script import Manager
from app import app


#定义应用程序实例
manager = Manager(app)

#启动程序
if __name__ == '__main__':
    #1.Flask集成的run方法是由werkzeug中的run_simple方法提供的。run()接受debug参数时，options.pop('debug')，
    #设定’use_reloader’默认参数为self.debug，’use_debugger’为self.debug.
    #manager.run()

    # 2.wsgiref：本质上是编写一个socket服务端，用于接收用户请求
    # from wsgiref.simple_server import make_server
    # server = make_server('', 5000, app)
    # server.serve_forever()

    from werkzeug.serving import run_simple
    #3.run_simple函数参数：hostname：应用程序的主机，port:端口，application：WSGI应用程序，use_reloader：如果程序代码修改，是否需要自动启动服务
    #use_debugger：程序是否要使用工具和调试系统/reloader_interval：秒重载器的间隔/reloader_type：重载器的类型
    #threaded：进程是否处理单线程的每次请求/processes：如果大于1，则在新进程中处理每个请求。达到这个最大并发进程数
    run_simple('192.168.31.5', 5000, app,threaded = True)
