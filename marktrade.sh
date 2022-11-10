#!/bin/bash

echo "streamlit run ..."
sudo chown 1000:1000 $HOME

echo 'shell /bin/bash' > $HOME/.screenrc
echo 'termcapinfo xterm* ti@:te@' >> $HOME/.screenrc

if [ $run_mode = 'release' ];
then
if [ -e $HOME/.pip/pip.conf ];
then
pip install --no-deps tickmine;
pip install --no-deps ticknature;
pip install --no-deps ctpview;
else
pip install --no-deps --index-url http://192.168.0.102:3141/root/dev tickmine --trusted-host 192.168.0.102;
pip install --no-deps --index-url http://192.168.0.102:3141/root/dev ticknature --trusted-host 192.168.0.102;
pip install --no-deps --index-url http://192.168.0.102:3141/root/dev ctpview --trusted-host 192.168.0.102;
fi
fi

if [ -e $HOME/.local/coredump ]; then echo ".local/coredump existed"; else mkdir $HOME/.local/coredump; fi
echo "$HOME/.local/coredump/core-%e-%p-%t"|sudo tee -a /proc/sys/kernel/core_pattern

if [ -e $HOME/.streamlit ]; then echo ".streamlit existed"; else mkdir $HOME/.streamlit; fi

if [ -e $HOME/.streamlit/config.toml ];
    then echo "config existed";
    else echo [server] >> $HOME/.streamlit/config.toml;
         echo port=8888 >> $HOME/.streamlit/config.toml;
         echo enableCORS=false >> $HOME/.streamlit/config.toml;
         echo address="\"0.0.0.0\"" >> $HOME/.streamlit/config.toml;
         echo baseUrlPath="\"$base_url\"" >> $HOME/.streamlit/config.toml;
         echo enableXsrfProtection=false >> $HOME/.streamlit/config.toml;
fi

sudo apt-get install -y marktrade

sudo chmod 777 /dev/mem
sudo chmod 777 /sys/firmware/dmi/tables/smbios_entry_point
sudo chmod 777 /sys/firmware/dmi/tables/DMI

if [ $run_mode = 'release' ];
then
ctpview_path=` python -c "import ctpview;print(ctpview.__path__[0])" `
nohup streamlit run $ctpview_path/workspace/ctp/domain/presentation.py >> $HOME/.streamlit/output.log 2>&1 &
fi

sudo ldconfig
nohup proxy </dev/null 1>/dev/null 2>/dev/null
