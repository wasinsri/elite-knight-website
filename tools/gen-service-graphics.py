#!/usr/bin/env python3
"""สร้างกราฟิก SVG สำหรับหน้าบริการ — ลายเส้นคลื่น (wave engraving) สีแบรนด์
ใช้: python3 tools/gen-service-graphics.py   (เขียนลง assets/img/)

ทุกหน้าใช้ลายเส้นชุดเดียวกัน ต่างกันที่รูปทรงกรอบ (shape) และสัญลักษณ์ตรงกลาง (emblem)
"""
import math, os

A, PANEL, LINE, INK = "#087568", "#f9fbfa", "#d7e3df", "#172c32"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")
CX, CY = 240, 200

# ---------------------------------------------------------------- shapes ----
def polygon(R, n, rot=-90, cx=CX, cy=CY, prec=1):
    pts = []
    for i in range(n):
        a = math.radians(rot + 360 * i / n)
        pts.append(f"{round(cx+R*math.cos(a),prec)},{round(cy+R*math.sin(a),prec)}")
    return "M" + " ".join(pts) + " Z"

def circle_path(R, cx=CX, cy=CY):
    return f"M{cx-R} {cy} a{R} {R} 0 1 0 {2*R} 0 a{R} {R} 0 1 0 {-2*R} 0 Z"

def roundrect(w, h, r, cx=CX, cy=CY):
    x, y = cx - w / 2, cy - h / 2
    return (f"M{x+r} {y} H{x+w-r} a{r} {r} 0 0 1 {r} {r} V{y+h-r} a{r} {r} 0 0 1 {-r} {r} "
            f"H{x+r} a{r} {r} 0 0 1 {-r} {-r} V{y+r} a{r} {r} 0 0 1 {r} {-r} Z")

SHIELD = ("M240 58 L372 100 V214 c0 62 -53 100 -132 128 c-79 -28 -132 -66 -132 -128 V100 Z",
          "M240 90 L340 122 V214 c0 46 -40 76 -100 97 c-60 -21 -100 -51 -100 -97 V122 Z",
          "M240 122 L308 144 V214 c0 31 -27 51 -68 66 c-41 -15 -68 -35 -68 -66 V144 Z")

# ------------------------------------------------------------ wave fills ----
def wline(x0, x1, amp, per, phase, steps, prec=1):
    """เส้นคลื่นรอบแกน y=0 — วางตำแหน่งจริงด้วย <use y=...> เพื่อให้ไฟล์เล็ก"""
    return "M" + " ".join(
        f"{round(x0+(x1-x0)*i/steps, prec)},{round(amp*math.sin(2*math.pi*per*i/steps+phase), prec)}"
        for i in range(steps + 1))

def field(idp, y0, y1, step, amp, per, steps, x0=52, x1=428, nphase=6, phase_step=0.95):
    defs = [f'<path id="{idp}{j}" d="{wline(x0,x1,amp,per,j*phase_step,steps)}"/>' for j in range(nphase)]
    uses, y, i = [], y0, 0
    while y <= y1:
        uses.append(f'<use href="#{idp}{i%nphase}" y="{round(y,1)}"/>')
        y += step; i += 1
    return "\n    ".join(defs), "\n      ".join(uses)

# ------------------------------------------------------------- hero card ----
def hero(name, shapes, emblem_paths, emblem_dots=()):
    outer, mid, core = shapes
    d_core, u_core = field("c", 34, 366, 3.1, 2.4, 6.1, 84)
    d_mid,  u_mid  = field("m", 34, 366, 7.0, 3.0, 3.8, 60)
    d_bg,   u_bg   = field("b", 34, 366, 11.0, 3.4, 1.8, 44)
    halo = "\n  ".join(f'<path d="{d}" fill="none" stroke="{PANEL}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>' for d in emblem_paths)
    mark = "\n  ".join(f'<path d="{d}" fill="none" stroke="{A}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>' for d in emblem_paths)
    dots_halo = "\n  ".join(f'<circle cx="{x}" cy="{y}" r="10.5" fill="{PANEL}"/>' for x, y in emblem_dots)
    dots = "\n  ".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{A}"/>' for x, y in emblem_dots)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 400" role="img" aria-hidden="true" focusable="false">
  <defs>
    <clipPath id="clipPanel"><rect x="40" y="26" width="400" height="348" rx="10"/></clipPath>
    <clipPath id="clipMid"><path d="{mid}"/></clipPath>
    <clipPath id="clipCore"><path d="{core}"/></clipPath>
    {d_bg}
    {d_mid}
    {d_core}
  </defs>

  <rect x="40" y="26" width="400" height="348" rx="10" fill="{PANEL}"/>
  <g clip-path="url(#clipPanel)" fill="none" stroke="{A}" stroke-width="0.8" stroke-opacity="0.11" stroke-linecap="round">
      {u_bg}
  </g>
  <rect x="40" y="26" width="400" height="348" rx="10" fill="none" stroke="{LINE}"/>

  <path d="{outer}" fill="none" stroke="{A}" stroke-width="1.4" stroke-opacity="0.22" stroke-linejoin="round"/>
  <g clip-path="url(#clipMid)" fill="none" stroke="{A}" stroke-width="0.9" stroke-opacity="0.34" stroke-linecap="round">
      {u_mid}
  </g>
  <path d="{mid}" fill="none" stroke="{A}" stroke-width="1.4" stroke-opacity="0.40" stroke-linejoin="round"/>

  <g clip-path="url(#clipCore)" fill="none" stroke="{A}" stroke-width="2.0" stroke-opacity="0.95" stroke-linecap="round">
      {u_core}
  </g>
  <path d="{core}" fill="none" stroke="{A}" stroke-width="1.6" stroke-opacity="0.85" stroke-linejoin="round"/>

  {halo}
  {dots_halo}
  {mark}
  {dots}

  <g fill="{PANEL}" stroke="{A}" stroke-width="1.6">
    <circle cx="108" cy="100" r="6"/><circle cx="372" cy="100" r="6"/><circle cx="240" cy="342" r="6"/>
  </g>
  <g fill="none" stroke="{A}" stroke-opacity="0.35" stroke-width="1.2" stroke-linecap="round">
    <path d="{wline(114,158,2.2,2.5,0,24)}" transform="translate(0 100)"/>
    <path d="{wline(322,366,2.2,2.5,0,24)}" transform="translate(0 100)"/>
  </g>
</svg>
'''
    p = os.path.join(OUT, name); open(p, "w").write(svg)
    return name, os.path.getsize(p)

# -------------------------------------------------------- approach strip ----
def wave_abs(x0, x1, y, amp, per, steps=180, phase=0.0, prec=1):
    return "M" + " ".join(
        f"{round(x0+(x1-x0)*i/steps,prec)},{round(y+amp*math.sin(2*math.pi*per*i/steps+phase),prec)}"
        for i in range(steps + 1))

def approach(name, labels):
    yb, amp, per = 36, 13, 1.5
    xs = [90, 352, 614, 876]
    wy = lambda x: yb + amp * math.sin(2 * math.pi * per * (x - 90) / 786)
    nodes = "\n".join(f'''  <g>
    <circle cx="{x}" cy="{wy(x):.1f}" r="18" fill="{A if i==3 else '#ffffff'}"{'' if i==3 else f' stroke="{A}" stroke-width="2.2"'}/>
    <text x="{x}" y="{wy(x)+5.5:.1f}" text-anchor="middle" font-size="14" font-weight="700" fill="{'#ffffff' if i==3 else A}">{i+1}</text>
    <text x="{x}" y="90" text-anchor="middle" font-size="15" font-weight="600" fill="{INK}" letter-spacing="0.02em">{lab}</text>
  </g>''' for i, (x, lab) in enumerate(zip(xs, labels)))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 100" role="img" aria-hidden="true" focusable="false" font-family="system-ui, -apple-system, 'Segoe UI', sans-serif">
  <defs>
    <linearGradient id="apTrack" gradientUnits="userSpaceOnUse" x1="90" y1="0" x2="876" y2="0">
      <stop offset="0" stop-color="{A}" stop-opacity="0.25"/>
      <stop offset="1" stop-color="{A}" stop-opacity="0.95"/>
    </linearGradient>
  </defs>
  <g fill="none" stroke-linecap="round">
    <path d="{wave_abs(90,876,yb+13,amp,per,180,phase=1.1)}" stroke="{A}" stroke-width="0.8" stroke-opacity="0.14"/>
    <path d="{wave_abs(90,876,yb+9,amp,per,180,phase=0.75)}" stroke="{A}" stroke-width="0.8" stroke-opacity="0.19"/>
    <path d="{wave_abs(90,876,yb+5,amp,per,180,phase=0.4)}" stroke="{A}" stroke-width="0.8" stroke-opacity="0.26"/>
    <path d="{wave_abs(90,876,yb,amp,per,240)}" stroke="url(#apTrack)" stroke-width="2.2"/>
  </g>
{nodes}
</svg>
'''
    p = os.path.join(OUT, name); open(p, "w").write(svg)
    return name, os.path.getsize(p)

# ----------------------------------------------------------------- pages ----
HEROES = {
    # โล่ — ความมั่นคงปลอดภัย
    "hero-cybersecurity.svg": (SHIELD, ["M215 209 l17 18 l36 -40"], []),
    # หกเหลี่ยม — โครงข่ายข้อมูล
    "hero-data-ai.svg": ((polygon(145, 6), polygon(110, 6), polygon(72, 6)),
                         ["M240 172 L204 226", "M240 172 L276 226", "M204 226 L276 226"],
                         [(240, 172), (204, 226), (276, 226)]),
    # วงกลม — การเปลี่ยนผ่าน
    "hero-digital-transformation.svg": ((circle_path(145), circle_path(110), circle_path(72)),
                                        ["M240 240 V166", "M212 194 L240 166 L268 194"], []),
    # สี่เหลี่ยมข้าวหลามตัด — โครงสร้างองค์กร
    "hero-management.svg": ((polygon(150, 4), polygon(114, 4), polygon(76, 4)),
                            ["M240 176 V198", "M198 198 H282", "M198 198 V222", "M282 198 V222"],
                            [(240, 170), (198, 228), (282, 228)]),
    # สี่เหลี่ยมมุมมน — พอร์ตโฟลิโอโครงการ
    "hero-strategic-pmo.svg": ((roundrect(264, 232, 18), roundrect(196, 172, 14), roundrect(128, 112, 10)),
                               ["M196 240 H284", "M210 240 V218", "M240 240 V196", "M270 240 V174"], []),
    # ห้าเหลี่ยม — 5 หมวดบริการ
    "hero-services.svg": ((polygon(148, 5), polygon(112, 5), polygon(74, 5)),
                          [f"M{CX} {CY} L{round(CX+44*math.cos(math.radians(-90+72*i)),1)} {round(CY+44*math.sin(math.radians(-90+72*i)),1)}" for i in range(5)],
                          [(CX, CY)] + [(round(CX + 44 * math.cos(math.radians(-90 + 72 * i)), 1),
                                         round(CY + 44 * math.sin(math.radians(-90 + 72 * i)), 1)) for i in range(5)]),
}

APPROACHES = {
    "approach-cybersecurity.svg": ["Assess", "Prioritize", "Roadmap", "Govern"],
    "approach-data-ai.svg": ["Discover", "Prioritize", "Design", "Enable"],
    "approach-digital-transformation.svg": ["Align", "Map", "Shape", "Mobilize"],
    "approach-management.svg": ["Frame", "Diagnose", "Design", "Embed"],
    "approach-strategic-pmo.svg": ["Baseline", "Design", "Mobilize", "Improve"],
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, (shapes, paths, dots) in HEROES.items():
        n, s = hero(name, shapes, paths, dots); total += s; print(f"{n:42s} {s:>7,} B")
    for name, labels in APPROACHES.items():
        n, s = approach(name, labels); total += s; print(f"{n:42s} {s:>7,} B")
    print(f"{'TOTAL':42s} {total:>7,} B")
