#!/usr/bin/env python3
"""Generates watchface/src/main/res/raw/watchface.xml (Watch Face Format).

The date row ("воскресенье 11.10" + battery icon) shows the day name in the
watch language. WFF cannot measure text width at runtime, so the row is
centered as if the day name were the long Russian "понедельник". Edit the constants below and re-run:
python3 tools/generate_watchface.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "watchface/src/main/res/raw/watchface.xml"

SIZE = 450  # WFF coordinate space; scaled to the real screen (Pixel Watch 3: 384/456 px)
CENTER = SIZE / 2

# Battery thresholds (percent, inclusive) and colors.
BATTERY_CRITICAL = 10
BATTERY_LOW = 25
COLOR_CRITICAL = "#FFFF453A"
COLOR_LOW = "#FFFFD60A"
COLOR_OK = "#FFFFFFFF"

DATE_FONT_SIZE = 30
DATE_Y, DATE_H = 92, 44
DATE_COLOR = "#FFE6E6E6"

BATTERY_W, BATTERY_H = 40, 20
BATTERY_GAP = 10

TIME_FONT_SIZE = 124
TIME_Y, TIME_H = 140, 150

COMP_D = 116
COMP_Y = 296
COMP_GAP = 16
# Inner layout below is drawn for a 78 px circle and scaled to COMP_D.
K = COMP_D / 78

# Day name used only to center the date row (a long one, so longer names fit);
# the watch renders [DAY_OF_WEEK_F] in its own language.
REFERENCE_DAY = "понедельник"

# Rough advance widths (in em) of a Google Sans-like font, used to center the date row.
_WIDE = set("жшщмыюфmwMW")
_NARROW = set("гтсрьзfirtjl")


def text_width(s: str, size: float) -> float:
    w = 0.0
    for ch in s:
        if ch in _WIDE:
            w += 0.74
        elif ch in _NARROW:
            w += 0.49
        elif ch.isdigit():
            w += 0.57
        elif ch in ". ":
            w += 0.27
        else:
            w += 0.54
    return w * size


def battery(x: float, y: float, color: str) -> str:
    return f"""\
            <PartDraw x="{x:.0f}" y="{y:.0f}" width="{BATTERY_W}" height="{BATTERY_H}">
              <RoundRectangle x="1" y="1" width="34" height="18" cornerRadiusX="4" cornerRadiusY="4">
                <Stroke color="{color}" thickness="2"/>
              </RoundRectangle>
              <RoundRectangle x="36" y="6" width="3.5" height="8" cornerRadiusX="1.5" cornerRadiusY="1.5">
                <Fill color="{color}"/>
              </RoundRectangle>
              <Rectangle x="4" y="4" width="28" height="12">
                <Fill color="{color}"/>
                <Transform target="width" value="clamp([BATTERY_PERCENT], 0, 100) * 0.28"/>
              </Rectangle>
            </PartDraw>"""


def battery_group(x: float, y: float) -> str:
    return f"""\
        <Condition>
          <Expressions>
            <Expression name="critical"><![CDATA[[BATTERY_PERCENT] <= {BATTERY_CRITICAL}]]></Expression>
            <Expression name="low"><![CDATA[[BATTERY_PERCENT] <= {BATTERY_LOW}]]></Expression>
          </Expressions>
          <Compare expression="critical">
{battery(x, y, COLOR_CRITICAL)}
          </Compare>
          <Compare expression="low">
{battery(x, y, COLOR_LOW)}
          </Compare>
          <Default>
{battery(x, y, COLOR_OK)}
          </Default>
        </Condition>"""


def date_row() -> str:
    text_w = text_width(f"{REFERENCE_DAY} 00.00", DATE_FONT_SIZE)
    row_w = text_w + BATTERY_GAP + BATTERY_W
    text_end = CENTER - row_w / 2 + text_w
    batt_x = text_end + BATTERY_GAP
    batt_y = DATE_Y + (DATE_H - BATTERY_H) / 2 + 1
    return f"""\
    <PartText x="0" y="{DATE_Y}" width="{text_end:.0f}" height="{DATE_H}">
      <Text align="END" ellipsis="TRUE">
        <Font family="SYNC_TO_DEVICE" size="{DATE_FONT_SIZE}" color="{DATE_COLOR}" weight="MEDIUM">
          <Template>%s %s.%s<Parameter expression="[DAY_OF_WEEK_F]"/><Parameter expression="[DAY_Z]"/><Parameter expression="[MONTH_Z]"/></Template>
        </Font>
      </Text>
    </PartText>
{battery_group(batt_x, batt_y)}"""


def comp_ring() -> str:
    return f"""\
          <PartDraw x="0" y="0" width="{COMP_D}" height="{COMP_D}">
            <Ellipse x="0" y="0" width="{COMP_D}" height="{COMP_D}">
              <Fill color="#FF161616"/>
            </Ellipse>
          </PartDraw>"""


def text_part(y: float, h: float, size: float, expr: str, color: str, weight: str = "NORMAL", pad: float = 10) -> str:
    y, h, size, pad = round(y * K), round(h * K), round(size * K), round(pad * K)
    return f"""\
          <PartText x="{pad}" y="{y}" width="{COMP_D - 2 * pad}" height="{h}">
            <Text align="CENTER" ellipsis="TRUE">
              <Font family="SYNC_TO_DEVICE" size="{size}" color="{color}" weight="{weight}">
                <Template>%s<Parameter expression="{expr}"/></Template>
              </Font>
            </Text>
          </PartText>"""


def image_part(size: float, y: float, source: str, tint: bool) -> str:
    size, y = round(size * K), round(y * K)
    x = (COMP_D - size) / 2
    tint_attr = ' tintColor="#FFFFFFFF"' if tint else ""
    return f"""\
          <PartImage x="{x:.0f}" y="{y:.0f}" width="{size}" height="{size}"{tint_attr}>
            <Image resource="{source}"/>
          </PartImage>"""


def complication_slot(slot_id: int, name: str, x: float, empty_label: str) -> str:
    d = COMP_D
    return f"""\
    <ComplicationSlot slotId="{slot_id}" displayName="{name}" x="{x:.0f}" y="{COMP_Y}" width="{d}" height="{d}"
        supportedTypes="SHORT_TEXT RANGED_VALUE MONOCHROMATIC_IMAGE SMALL_IMAGE EMPTY" isCustomizable="TRUE">
      <DefaultProviderPolicy defaultSystemProvider="EMPTY" defaultSystemProviderType="EMPTY"/>
      <BoundingOval x="0" y="0" width="{d}" height="{d}"/>
      <Variant mode="AMBIENT" target="alpha" value="0"/>
      <Complication type="SHORT_TEXT">
{comp_ring()}
{image_part(24, 9, "[COMPLICATION.MONOCHROMATIC_IMAGE]", True)}
{text_part(31, 26, 21, "[COMPLICATION.TEXT]", "#FFFFFFFF", "MEDIUM", pad=6)}
{text_part(54, 16, 13, "[COMPLICATION.TITLE]", "#FFB0B0B0", pad=16)}
      </Complication>
      <Complication type="RANGED_VALUE">
{comp_ring()}
          <PartDraw x="0" y="0" width="{d}" height="{d}">
            <Arc centerX="{d // 2}" centerY="{d // 2}" width="{d - 6}" height="{d - 6}" startAngle="0" endAngle="360">
              <Stroke color="#FFFFFFFF" thickness="{round(4 * K)}" cap="ROUND"/>
              <Transform target="endAngle"
                  value="360 * clamp(([COMPLICATION.RANGED_VALUE_VALUE] - [COMPLICATION.RANGED_VALUE_MIN]) / clamp([COMPLICATION.RANGED_VALUE_MAX] - [COMPLICATION.RANGED_VALUE_MIN], 0.0001, 1000000000), 0, 1)"/>
            </Arc>
          </PartDraw>
{image_part(22, 11, "[COMPLICATION.MONOCHROMATIC_IMAGE]", True)}
{text_part(33, 26, 20, "[COMPLICATION.TEXT]", "#FFFFFFFF", "MEDIUM", pad=8)}
      </Complication>
      <Complication type="MONOCHROMATIC_IMAGE">
{comp_ring()}
{image_part(38, 20, "[COMPLICATION.MONOCHROMATIC_IMAGE]", True)}
      </Complication>
      <Complication type="SMALL_IMAGE">
{comp_ring()}
{image_part(46, 16, "[COMPLICATION.SMALL_IMAGE]", False)}
      </Complication>
      <Complication type="EMPTY">
{comp_ring()}
          <PartText x="4" y="{d // 2 - 14}" width="{d - 8}" height="28">
            <Text align="CENTER">
              <Font family="SYNC_TO_DEVICE" size="{round(15 * K)}" color="#FF7A7A7A">{empty_label}</Font>
            </Text>
          </PartText>
      </Complication>
    </ComplicationSlot>"""


def build() -> str:
    left_x = CENTER - COMP_GAP / 2 - COMP_D
    right_x = CENTER + COMP_GAP / 2
    return f"""\
<?xml version="1.0" encoding="utf-8"?>
<!-- GENERATED by tools/generate_watchface.py - edit the generator, not this file. -->
<WatchFace width="{SIZE}" height="{SIZE}">
  <Metadata key="CLOCK_TYPE" value="DIGITAL"/>
  <Metadata key="PREVIEW_TIME" value="10:08:32"/>
  <Scene backgroundColor="#FF000000">

    <!-- Day of week (watch language) + DD.MM + battery indicator -->
{date_row()}

    <!-- Current time -->
    <DigitalClock x="0" y="{TIME_Y}" width="{SIZE}" height="{TIME_H}">
      <TimeText format="hh:mm" hourFormat="24" align="CENTER" x="0" y="0" width="{SIZE}" height="{TIME_H}">
        <Font family="SYNC_TO_DEVICE" size="{TIME_FONT_SIZE}" color="#FFFFFFFF" weight="BOLD"/>
      </TimeText>
      <Variant mode="AMBIENT" target="alpha" value="190"/>
    </DigitalClock>

    <!-- UV index (left) and timer (right): tap opens the source app -->
{complication_slot(0, "UV", left_x, "УФ")}
{complication_slot(1, "Timer", right_x, "Таймер")}
  </Scene>
</WatchFace>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT}")
