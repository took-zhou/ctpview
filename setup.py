from setuptools import setup, find_packages
# file: setup.py

setup(
    name="ctpview",
    version="1.2.2",
    author="zhoufan",
    author_email="zhoufan@cdsslh.com",

    keywords='presentation layer',

    # 项目的依赖库，读取的requirements.txt内容
    install_requires = [
        'streamlit>=0.88.0',
        'numpy>=1.19.5',
        'psutil>=5.8.0',
        'pandas>=1.1.5',
        'zerorpc>=0.6.3'
    ],

    # 项目主页
    url="http://devpi.cdsslh.com:8090",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages()
)
