# Standalone flipper-zero plugins in embedded rust


This repo demonstrates compiling a flipper-zero app in rust, then using unholy linker incantations to smooze it into an elf file that fz can load.

This is terrible dont use this.

## Under the hood

1. Rust crate uses the amazing [flipper-zero crates](https://github.com/dcoles/flipperzero-rs) by [dcoles](https://github.com/dcoles), compiling to an intermediate `.a` with a fixed `plugin_start` identifier for the entrypoint.
2. (build.sh) Unholy invocation of gcc to compile the rustc-generated archive to an ELF the fz can work with.
3. (gen_fapmeta.py) Generates the weird `.fapmeta` ELF section that tells the loader about what SDK version its compiled against as well as the app name and other crap.
4. (build.sh) objcopy incantation to strip binary bloat and weave in the generated fapmeta section.

## To build

Assuming a NixOS system:

```shell
nix-shell
./build.sh
# The binary should now be in target/thumbv7em-none-eabihf/release/libfz_rust.fap
```

## License / thanks

Look, do whatever lol. The bits I copied from the flipperzero sauce are licensed GNUv3 and marked appropriately. The bits i copied from dcoles are MIT and marked
appropriately. Everything else, lets just say its dual GNUv3 & MIT.

Mad props to [dcoles](https://github.com/dcoles) for making the crates for binding to the SDK, as well as the example code I copypasta'd. The only novel bit
in this repo is building a fap file without needing a copy of the firmware and a working firmware toolchain.