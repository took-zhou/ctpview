import os
import sys
import streamlit_authenticator as stauth


def make_protoc():
    '''
    编译protoc文件
    '''
    path = './../../workspace/common/protobuf'
    protoc_path = "protoc/bin/protoc"
    message_path = "message"
    package_name = ['ctpview', 'market', 'trader']
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


def make_md5():
    '''
    生产md5密码
    '''
    hashed_passwords = stauth.Hasher([sys.argv[2]]).generate()
    print(hashed_passwords[0])


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "protoc":
        make_protoc()
    elif len(sys.argv) == 3 and sys.argv[1] == 'md5':
        make_md5()
