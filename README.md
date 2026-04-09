# Pico Packages

These are conan packages for the Pico SDK for the Raspberry Pi Pico family of
microcontrollers.

## CI Deployed Packages

### Tool Packages

### OS Tools

For Mac and Linux

- libusb:
  - 1.0.26

> [!WARNING]
> Windows development is currently not supported

### PicoSDK Packages

Versions:

- 2.1.1
- 2.2.0

Packages contained:

- pioasm
- picotool/pioasm/pico-sdk:

## Building the Packages

First build the tool packages needed for picosdk to build PIO assembly code

```bash
conan create pioasm --version=2.2.0 -pr:a hal/tc/llvm -b missing
conan create piosdk --version=2.2.0
conan create picotool --version=2.2.0 -pr:a hal/tc/llvm -b missing
```

For macOS add `-pr:a profiles/macos-build` in order to ensure that the LLVM
toolchain gets its sysroot set.
