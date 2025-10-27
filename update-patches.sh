VERSION=0.10.1
git diff opendbc_repo/opendbc/safety/modes/gm.h > $VERSION-panda.patch
git diff opendbc_repo/opendbc/car/car_helpers.py > $VERSION-car_helpers.patch
git diff opendbc_repo/opendbc/car/gm/carcontroller.py > $VERSION-carcontroller.patch
git diff opendbc_repo/opendbc/car/gm/interface.py > $VERSION-interface.patch
git diff launch_openpilot.sh > $VERSION-launch_openpilot.patch
git diff opendbc_repo/opendbc/car/gm/values.py > $VERSION-values.patch
