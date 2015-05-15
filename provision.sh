apt-get update
apt-get upgrade
apt-get install -y build-essential software-properties-common git libboost-all-dev
if [ ! -d "vowpal_wabbit" ]; then
    git clone git://github.com/JohnLangford/vowpal_wabbit.git
fi
cd vowpal_wabbit
git fetch
echo "Checking out $VW_COMMIT_HASH"
git checkout "$VW_COMMIT_HASH"
make clean
make
make install