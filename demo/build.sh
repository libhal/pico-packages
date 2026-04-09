set -ex

conan build . -pr:h=../profiles/rp2350 -pr:h=arm-gcc-12.3 -nr --build=missing  -of build
