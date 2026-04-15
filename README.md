# Pico Packages

This repository contains conan package files for the Raspberry Pi Pico C/C++
SDK. This repository also seperately packages `pioasm` and `picotool` seperately
such that they may be consumed by conan packages as tool requirements. Various
patches are included so picosdk works better with conan dependencies.

## Building

`pico-sdk` is a pure source package and does not require any profile to build.
Use `conan create pico-sdk --version <version>` and it should just work. The current
version that is supported is `2.2.1-alpha` since it has hard-floating point ABI support.
`2.2.0` is also supported for soft-fp ABI, and is required to build picotool and pioasm.

```sh
conan create pico-sdk --version 2.2.1-alpha
```

`picotool` is a host software used to generate uf2 files and upload firmware. Use either
the default conan profile, or whatever conan profile you use to build host software. `picotool`
is currently tested to work on `2.2.0`, which depends on `pico-sdk/2.2.0`.

```sh
conan create picotool --version 2.2.0
```

`pioasm` is a host software used to assemble pio programs. It is not necessary unless you are
developing programs using the pio peripheral. `pioasm` is currently known to build on `2.2.0`, which
depends on `pico-sdk/2.2.0`.

```sh
conan create pioasm --version 2.2.0
```

`test_package` is a small program demonstrating the usage of `pico-sdk` and `picotool`. It is intended
as a guide on configuring dependents on how to use `pico-sdk`.

```sh
conan build test_package -pr:h hal/tc/arm-gcc-14.2 -pr:h feather-rp2350 -of build
```

Using `pico-sdk/2.2.1-alpha` with `picotool/2.2.0` is perfectly acceptable and the expected way to build
projects until `pico-sdk/2.2.1` becomes formally released.
