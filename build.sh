set -xe

cargo clean && cargo build --release --verbose

CRATE_SANITIZED_NAME="libfz_rust"
APP_NAME="yeetus maximus"

arm-none-eabi-gcc -o "target/thumbv7em-none-eabihf/release/${CRATE_SANITIZED_NAME}.elf" \
	-mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16 -mlittle-endian -mthumb \
	-Tmemory.x \
	-Ur -Wl,-Ur -Bsymbolic -nostartfiles -mlong-calls -fno-common -nostdlib -Wl,--gc-sections -Wl,--no-export-dynamic -fvisibility=hidden \
	-Wl,-eplugin_start -Xlinker -Map="target/thumbv7em-none-eabihf/release/${CRATE_SANITIZED_NAME}.elf.map" \
	-specs=nano.specs -specs=nosys.specs "target/thumbv7em-none-eabihf/release/${CRATE_SANITIZED_NAME}.a"

# Generate fapmeta: see https://github.com/flipperdevices/flipperzero-firmware/blob/873e1f114b7ca55a72dc68bf1b1fa6d169e7c17e/site_scons/fbt/elfmanifest.py
# 'Base header': [magic u32, manifest version u32, api version u32, hardware target u16]
# 'Application manifest': [stack size u16, app version u32, app name 32bytes padded with zeros, icon present bool in 1 byte, 32 bytes of icon data or omitted]
python gen_fapmeta.py "${APP_NAME}"

arm-none-eabi-objcopy \
	--remove-section .ARM.attributes --add-section .fapmeta=target/thumbv7em-none-eabihf/release/fapmeta --set-section-flags .fapmeta=contents,noload,readonly,data \
	--strip-debug --strip-unneeded "target/thumbv7em-none-eabihf/release/${CRATE_SANITIZED_NAME}.elf" "target/thumbv7em-none-eabihf/release/${CRATE_SANITIZED_NAME}.fap"