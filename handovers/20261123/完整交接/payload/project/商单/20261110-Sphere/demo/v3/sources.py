"""UI source images + coordinates for the v2 demo.

All rects are (x0, y0, x1, y1) in the pixel space of the image they belong to.
"lo" images are 100% zoom full-screen grabs (1920x1200 on display :10);
"hi" images are 175% zoom grabs used only inside the loupe card.
Swap PLACEHOLDER=False once raw_A stills are extracted.
"""
from pathlib import Path

ROOT = Path("/workspace/xhs/商单/20261110-Sphere/demo")
R4 = ROOT / "grabs/r4_stills"
A = ROOT / "v2/stills"           # raw_A extracts land here

PLACEHOLDER = False

if PLACEHOLDER:
    LO = {
        "overview": R4 / "overview.png",
        "avatar": R4 / "avatar_dialog.png",
        "reading": R4 / "reading_dialog.png",
    }
    HI = {   # placeholder: same 1x images (soft in loupe)
        "avatar_hi": R4 / "avatar_dialog.png",
        "reading_hi": R4 / "reading_dialog.png",
    }
    # areas to paint with page background before use (stray system cursor etc.)
    PAINT = {
        "overview": [((1700, 100, 1730, 135), (255, 255, 255))],
    }
    LOGO = (22, 103, 52, 133)
    # E-level crop of the overview page (inside the browser viewport)
    E_CROP = (0, 88, 1730, 1100)
    CARD1 = (288, 232, 512, 610)       # 我的数字形象 · 创建数字形象
    CARD2 = (288, 680, 662, 762)       # 我的声音 · 创建声音
    # avatar modal
    AV_MODAL = (510, 367, 1410, 877)
    AV_UPLOAD_COL = (530, 433, 952, 750)      # 手机上传 + 从电脑上传
    AV_PHOTOS = (968, 433, 1390, 750)         # sample photos (维港) → darken
    AV_REQ_BAR = (530, 758, 1390, 800)
    # reading dialog
    RD_MODAL = (560, 358, 1360, 888)
    RD_TEXT_COVER = (580, 530, 1340, 762)     # 朗读文本 (含「香港」) → frosted
    RD_COLUMN = (580, 530, 1340, 860)         # text + button + hint
    # loupe details: hi image, hi rect, matching lo rect, red target (hi coords)
    DETAILS = {
        "upload_row": dict(hi="avatar_hi", hi_rect=(530, 436, 952, 580),
                           lo_rect=(530, 436, 952, 580), red=(830, 487, 928, 531),
                           label="上传方式"),
        "req_bar": dict(hi="avatar_hi", hi_rect=(530, 752, 962, 806),
                        lo_rect=(530, 752, 962, 806), red=None, label="照片要求",
                        feather_r=True),
        "rec_btn": dict(hi="reading_hi", hi_rect=(742, 766, 1178, 866),
                        lo_rect=(742, 766, 1178, 866), red=(910, 782, 1010, 813),
                        label="开始录制", feather_l=True, feather_r=True),
    }
    HI_COVERS = {"reading_hi": [RD_TEXT_COVER]}
    HI_DARKEN = {"avatar_hi": [AV_PHOTOS]}
    HI_SCALE = 1.0
    REC_CURSOR = (1030, 800)
else:
    # raw_A.mp4 stills (fullscreen page, no browser chrome). Frame times in seconds:
    # overview 84, card1_hover 100, avatar 120 (100%), card2_hover 248, reading 276 (100%),
    # avatar_hi 184 (175%), reading_hi 412 (175%).
    LO = {k: A / f"{k}.png" for k in ("overview", "card1_hover", "card2_hover", "avatar", "reading")}
    HI = {"avatar_hi": A / "avatar_hi.png", "reading_hi": A / "reading_hi.png"}
    _cur = (1704, 96, 1734, 130)       # parked system cursor (top-right)
    PAINT = {k: [(_cur, "sample")] for k in LO}
    LOGO = (14, 12, 48, 46)
    E_CROP = (0, 0, 1730, 1012)
    CARD1 = (287, 145, 511, 523)
    CARD2 = (286, 590, 661, 675)
    AV_MODAL = (510, 344, 1410, 856)
    AV_UPLOAD_COL = (531, 411, 951, 726)
    AV_PHOTOS = (968, 411, 1389, 726)
    AV_REQ_BAR = (531, 740, 1389, 778)
    RD_MODAL = (560, 336, 1360, 864)
    RD_TEXT_COVER = (580, 505, 1340, 740)
    RD_COLUMN = (580, 503, 1339, 844)
    DETAILS = {
        "upload_row": dict(hi="avatar_hi", hi_rect=(306, 340, 946, 540),
                           lo_rect=(525, 427, 951, 560), red=(775, 402, 902, 452), label="上传方式"),
        "req_bar": dict(hi="avatar_hi", hi_rect=(306, 800, 946, 884),
                        lo_rect=(525, 735, 951, 785), red=None, label="照片要求", feather_r=False),
        "rec_btn": dict(hi="reading_hi", hi_rect=(680, 806, 1232, 962),
                        lo_rect=(773, 738, 1141, 842), red=(890, 840, 1032, 884),
                        label="开始录制", feather_l=True, feather_r=True),
    }
    HI_COVERS = {"reading_hi": [(395, 470, 1525, 810)]}
    HI_DARKEN = {"avatar_hi": [(970, 316, 1600, 790)]}
    HI_SCALE = 1.5
    REC_CURSOR = (1185, 772)
