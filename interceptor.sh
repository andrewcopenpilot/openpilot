git pull origin
git checkout v0.10.0
git submodule update
patch -p1 < 0.10-panda.patch
cd panda
scons
cp board/obj/panda.bin.signed /data/panda
cd /data/openpilot

git checkout origin/release3
rm panda/board/obj/panda.bin.signed
cp ../panda.bin.signed panda/board/obj/panda.bin.signed
patch -p1 < 0.10-carhelpers.patch
patch -p1 < 0.10-carcontroller.patch
patch -p1 < 0.10-interface.patch
patch -p1 < 0.10-launch_openpilot.patch
patch -p1 < 0.10-values.patch

cp github_init_ssh.sh

git checkout -b [release]-release3-gm-ascm-interceptor-volt
git add -f panda/board/obj/panda.bin.signed
git add --all

git remote add fork https://github.com/andrewcopenpilot/openpilot.git
git push fork

update-patches.sh
