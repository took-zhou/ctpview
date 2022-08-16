import os
import sys


def make_protoc():
    '''
    编译protoc文件
    '''
    path = './../../workspace/common/protobuf'
    protoc_path = "protoc/bin/protoc"
    message_path = "message"
    package_name = ['ctpview']
    touch_list = []
    os.chdir(path)
    version = os.popen('%s --version' % (protoc_path)).readlines()
    print(version[0])
    for root, dirs, files in os.walk(message_path):
        for f in files:
            for item in package_name:
                if item in f and f.split('.')[-1] == 'proto' and f not in touch_list:
                    filename = os.path.join(root, f)
                    touch_list.append(f)
                    command = "%s -I=%s --python_out . %s" % (protoc_path, message_path, filename)
                    print(command)
                    os.system(command)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "protoc":
        make_protoc()
