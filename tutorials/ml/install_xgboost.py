# Guide to installing xgboost

# Reference:
#https://isaacchanghau.github.io/2017/06/20/Install-XGBoost-on-Mac-OS-X/

#Uninstall all versions of gcc, so that we know which version is being referenced
brew uninstall gcc
#Then reinstall
brew install gcc --without-multilib

#Clone xgboost repo
git clone --recursive https://github.com/dmlc/xgboost
#Build repo
cd xgboost
vi make/config.mk
#Open config File and uncomment and change the following lines
export CC = gcc-5
export CXX = g++-5
# Then build repo
cp make/config.mk .
sudo make -j4 # sudo is important, prevent permission denied issue

#Once the above is done, following python package installing here:
#http://xgboost.readthedocs.io/en/latest/build.html#python-package-installation
cd python-package; sudo python setup.py install

#add python page to python path
export PYTHONPATH=~/xgboost/python-package

#navigate to python package and install
cd python-package; python setup.py develop --user
