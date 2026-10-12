# Pin2 Циферблат — Wear OS watch face (Pixel Watch 3)

A [Watch Face Format](https://developer.android.com/training/wearables/wff) watch face
(resource-only APK, no code — the only kind Wear OS 6+/7 accepts):

```
     воскресенье 11.10 ▭      ← day in watch language + DD.MM + battery icon
          10:08               ← time, 24h
       ( УФ )  (Таймер)       ← tappable complications: UV index, timer
```

* **Battery icon** fill shows the charge level. Color: **red** ≤ 10 %, **yellow** ≤ 25 %, **white** otherwise.
* **Day name follows the watch language** (Settings → System → Languages).
* **UV / timer** are complication slots: they show live data, and a tap opens the source app.
* In always-on (ambient) mode the complications are hidden and the time is dimmed.

## Project layout

| Path | What |
|---|---|
| `watchface/src/main/res/raw/watchface.xml` | The watch face (generated — don't edit by hand) |
| `tools/generate_watchface.py` | Generator: thresholds, colors, sizes, layout |
| `tools/RenderPreview.java` | Renders `res/drawable-nodpi/preview.png` (picker thumbnail) |
| `watchface/src/main/AndroidManifest.xml` | `hasCode=false`, WFF version 2 |

Change something → `python3 tools/generate_watchface.py` → rebuild.

## Build

```sh
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
./gradlew :watchface:assembleRelease
```

Output: `watchface/build/outputs/apk/release/watchface-release.apk` (signed with your local debug key).

## Install on the Pixel Watch 3

Below, `adb` means `~/Library/Android/sdk/platform-tools/adb`
(or add `~/Library/Android/sdk/platform-tools` to your `PATH`).

### 1. Enable developer options on the watch

1. **Settings → System → About → Versions**.
2. Tap **Build number** 7 times until you see “You are now a developer”.

### 2. Turn on wireless debugging

1. Make sure the watch and the Mac are on the **same Wi‑Fi network**.
2. **Settings → Developer options** → turn on **ADB debugging**.
3. Turn on **Wireless debugging** (allow when asked).
4. Tap **Pair new device**. The watch shows a pairing code and `IP:port`.

### 3. Pair and connect from the Mac

```sh
adb pair 192.168.1.50:41235 123456     # IP:port and code from the "Pair new device" screen
adb connect 192.168.1.50:39557         # IP:port from the main "Wireless debugging" screen (different port!)
adb devices                             # the watch should be listed as "device"
```

### 4. Install

```sh
adb install -r watchface/build/outputs/apk/release/watchface-release.apk
```

You should see `Success`.

### 5. Select the watch face

1. Long-press the current watch face.
2. Swipe left to the end and tap **+ Add** (Добавить).
3. Find **Pin2 Циферблат** in the list (usually under “Downloaded”) and tap it.

### 6. Assign the UV index and timer

1. Long-press the watch face → **Customize** (Настроить).
2. Swipe to the **complications** screen.
3. Tap the **left** slot → **Weather** → **UV index**.
4. Tap the **right** slot → **Timer** (from the Clock app).
5. Press the crown to save.

Until assigned, the slots show the grey labels “УФ” and “Таймер”.

### Done — turn debugging back off

**Settings → Developer options** → turn off **Wireless debugging** and **ADB debugging** (it drains the battery).

## Update / uninstall

```sh
# after rebuilding — same steps 2–3 to reconnect, then:
adb install -r watchface/build/outputs/apk/release/watchface-release.apk
# remove:
adb uninstall com.pin.pin2twf.watchface
```

## Troubleshooting

* **`INSTALL_FAILED_UPDATE_INCOMPATIBLE`** — an older build was signed with a different key: `adb uninstall com.pin.pin2twf.watchface`, then install again.
* **`adb pair` fails** — the pairing code/port expires after leaving the pairing screen; reopen **Pair new device** and retry.
* **Watch face shows a blank/black screen** — check the log: `adb logcat | grep -i watchface`.
* **No UV index complication offered** — open the Weather app on the watch once so it fetches data and allow location.
