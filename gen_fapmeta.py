#                    GNU GENERAL PUBLIC LICENSE
#                       Version 3, 29 June 2007
# 
# Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.
#
# See LICENSE in https://github.com/flipperdevices/flipperzero-firmware for full text.

import argparse
import os
import struct


_MANIFEST_MAGIC = 0x52474448
_API_VERSION = 0x00030000
_HARDWARE_TARGET_ID = 0x07

class ElfManifestBaseHeader(object):
    manifest_version: int
    api_version: int
    hardware_target_id: int
    manifest_magic: int

    def __init__(self, **kwargs):
        self.manifest_version = kwargs.get('manifest_version', 1)
        self.api_version = kwargs.get('api_version', _API_VERSION)
        self.hardware_target_id = kwargs.get('hardware_target_id', _HARDWARE_TARGET_ID)
        self.manifest_magic = kwargs.get('manifest_magic', _MANIFEST_MAGIC)

    def as_bytes(self):
        return struct.pack(
            "<IIIh",
            self.manifest_magic,
            self.manifest_version,
            self.api_version,
            self.hardware_target_id,
        )


class ElfManifestV1(object):
    stack_size: int
    app_version: int
    name: str = ""
    icon: bytes = b""

    def __init__(self, **kwargs):
        self.stack_size = kwargs.get('stack_size', 0x0400)
        self.app_version = kwargs.get('app_version', 0)
        self.name = kwargs.get('name', "Unnamed")
        self.icon = kwargs.get('icon', b"")


    def as_bytes(self):
        return struct.pack(
            "<hI32s?32s",
            self.stack_size,
            self.app_version,
            bytes(self.name.encode("ascii")),
            bool(self.icon),
            self.icon,
        )

parser = argparse.ArgumentParser(description="Generats the FAP metadata file.")
parser.add_argument("name", type=str)
args = parser.parse_args()

with open("target/thumbv7em-none-eabihf/release/fapmeta", "wb") as f:
    out = ElfManifestBaseHeader().as_bytes()
    out += ElfManifestV1(
            name = args.name,
        ).as_bytes()
    f.write(out)