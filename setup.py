from setuptools import find_packages, setup

# file: setup.py

setup(
    name="ctpview",
    version="1.7.7",
    author="zhoufan",
    author_email="zhoufan@cdsslh.com",
    keywords='presentation layer',
    data_files=[('ctpview', ['ctpview/project/projroot/config.json']), ('resource', ['ctpview/workspace/resource/icon.png'])],

    # 项目的依赖库，读取的requirements.txt内容
    install_requires=[
        'pandas>=1.4.3', 'plotly>=5.15.0', 'protobuf>=3.20.1', 'psutil>=5.9.1', 'pyzmq>=23.2.1', 'setuptools>=39.0.1', 'streamlit>=1.28.1',
        'streamlit_authenticator>=0.2.3', 'streamlit_autorefresh>=1.0.1'
    ],

    # 项目主页
    url="http://192.168.0.106:3141",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages())
