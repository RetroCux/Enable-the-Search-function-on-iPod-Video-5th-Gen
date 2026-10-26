# iPod Video 5G — enable the hidden Search function

[![Support on Ko-fi](https://img.shields.io/badge/Ko--fi-Support-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/RetroCux)

> One-byte patch to the stock Apple firmware. No Rockbox, no custom OS.

The **Search** function has been part of the iPod Video firmware since version
1.2 (September 2006), but it is only shown on the 5.5G: at runtime the firmware
reads the hardware revision and decides whether to enable it. This patch
changes a single byte of the `osos` image so that Search is enabled on the 5G
as well.

---

## Supported firmware

| Firmware | Family | Status |
|:--|:--|:--|
| **1.3** | 13, 20 | ✅ Tested on hardware (5G 60 GB) |
| **1.2.1** | 13 | ⚠️ Patch verified by static analysis (not tested on hardware) |
| 1.2.3 | 13 | ⚠️ Not verified |
| 1.0 – 1.1.2 | 13 | ❌ Not applicable: Search was introduced in 1.2 |

Tested on Ubuntu 26.04. Compatibility with iTunes, and the effect of iTunes on
a patched iPod, have not been tested.

---

## How it works

The `patch.py` script identifies the firmware image by SHA-1 and flips the one byte that
corresponds to that version. On an unknown image it writes nothing. Only the
versions listed above are supported.

---

## Requirements

| What | Notes |
|:--|:--|
| iPod Video 5G (30/60 GB) or 5G Late | Must **already run** the firmware version you patch (1.2.1 or 1.3). If it runs an older version, update it with iTunes first: the `osos` image has to match the resources already on the device. |
| Linux + Python 3 | Tested on Ubuntu |
| `ipodpatcher` (Rockbox) | Official builds for Linux, Windows and macOS: [download.rockbox.org/bootloader/ipod/ipodpatcher/](https://download.rockbox.org/bootloader/ipod/ipodpatcher/) (tested on Linux x86-64) |
| Firmware IPSW for your version | e.g. `iPod_13.1.3.ipsw`, from the Apple links listed at [theapplewiki.com/wiki/Firmware/iPod](https://theapplewiki.com/wiki/Firmware/iPod) |

---

## Procedure

The example uses firmware 1.3 (`iPod_13.1.3.ipsw`); adjust the file names for
other versions.

### 1. Build the patched image
```bash
unzip iPod_13.1.3.ipsw
python3 patch.py Firmware-13.6.3
```
Output: `Firmware-13.6.3-search.bin`, the patched `osos` image used below.

### 2. Put the iPod in Disk Mode
Unplug the iPod. Hold **Menu + Select** until the Apple logo appears, then
immediately hold **Select + Play** until the *Disk Mode* screen appears.
Plug it into the PC.

### 3. Unmount the data partition
In these examples the iPod appears as `/dev/sda`; on your computer it may be a
different device (`sdb`, `sdc`, …). Run `lsblk` and look for a disk the size of
your iPod whose first partition is about 110 MB, then replace `sda` with your
device in this and all the following commands.
```bash
lsblk                      # find the iPod (e.g. sda: sda1 ≈110 MB, sda2 = music)
sudo umount /dev/sda2
```

### 4. Back up and verify
```bash
chmod +x ipodpatcher
sudo ./ipodpatcher -rfb backup.bin              # keep this file in a safe place
sha1sum backup.bin
cmp -l backup.bin Firmware-13.6.3-search.bin    # must print exactly ONE line
```
Expected SHA-1 of the stock `osos`:

| Firmware | SHA-1 |
|:--|:--|
| 1.3 | `3281abc9f44bb8ddfa4e00da03488308fe624c53` |
| 1.2.1 | `b0a3c5ed5866563cc5b185d777b8f81ba17c4ab1` |

This confirms the iPod runs the same stock version you patched.
**If the hash differs or `cmp` prints more than one line, stop here.**

### 5. Write the patched image
```bash
sudo ./ipodpatcher -wfb Firmware-13.6.3-search.bin
```

### 6. Reboot
Eject the iPod from the file manager (or `sudo eject /dev/sda`), unplug it and
reboot with **Menu + Select**. Open **Music**: Search is the last item.

---

## Where to find Search

- **Music → Search** — last item of the Music menu.
- **Main menu** — *Settings → Main Menu → Search → On*. After changing it, put
  the iPod to sleep (hold **Play/Pause**) so the setting is saved to disk:
  settings changed right before a hard reset (Menu + Select) are lost, as with
  any iPod setting.

---

## Rollback

From Disk Mode:
```bash
sudo ./ipodpatcher -wfb backup.bin
```
Alternatively, Restore the iPod with iTunes, which also erases the music on it.

The patch itself writes only the firmware partition: Disk Mode, which lives in
flash, and the music partition are never touched.

---

## Notes

- Do **not** redistribute `.bin` files: they contain Apple firmware. The script
  contains no Apple code.
- An iTunes firmware update or Restore replaces the `osos` image with the stock
  one, so Search disappears. Just re-apply the patch afterwards.

## Disclaimer

Unofficial procedure, provided as is, without any warranty. Modifying firmware
may require a Restore, which erases the music on the iPod. The author accepts no responsibility for damage to
devices or loss of data. Proceed at your own risk.
