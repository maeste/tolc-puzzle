import math
import random

from exercises.base import Exercise


def _fmt(value, decimals=2):
    """Format a numeric value: show as int if whole, otherwise round."""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return str(round(value, decimals))


def _distractor(correct, spread=None, count=4):
    """Generate plausible numeric distractors around the correct value."""
    if spread is None:
        spread = max(1.0, abs(correct) * 0.25)
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        attempts += 1
        offset = random.uniform(-spread, spread)
        d = round(correct + offset, 2)
        if d > 0 and abs(d - correct) > 0.01:
            formatted = _fmt(d)
            if formatted != _fmt(correct):
                distractors.add(formatted)
    # fallback if not enough
    while len(distractors) < count:
        d = round(correct * random.uniform(0.5, 1.8), 2)
        if d > 0:
            formatted = _fmt(d)
            if formatted != _fmt(correct):
                distractors.add(formatted)
    return list(distractors)[:count]


def _distractor_signed(correct, spread=None, count=4):
    """Generate plausible numeric distractors that can be negative or zero.

    Used for transformation exercises where answers may be negative.
    """
    if spread is None:
        spread = max(2.0, abs(correct) * 0.4)
    distractors = set()
    correct_formatted = _fmt(correct)
    attempts = 0
    while len(distractors) < count and attempts < 300:
        attempts += 1
        offset = random.uniform(-spread, spread)
        d = round(correct + offset, 2)
        if abs(d - correct) > 0.01:
            formatted = _fmt(d)
            if formatted != correct_formatted:
                distractors.add(formatted)
    # Common sign-error distractors as fallback
    sign_variants = [
        -correct,
        correct + 1,
        correct - 1,
        correct * 2,
        -correct + 1,
        -correct - 1,
    ]
    for sv in sign_variants:
        if len(distractors) >= count:
            break
        formatted = _fmt(sv)
        if formatted != correct_formatted:
            distractors.add(formatted)
    # final fallback
    while len(distractors) < count:
        d = round(correct + random.uniform(-10, 10), 2)
        formatted = _fmt(d)
        if formatted != correct_formatted:
            distractors.add(formatted)
    return list(distractors)[:count]


# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

def _svg_start(width=300, height=250):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" '
        f'style="font-family:Arial,sans-serif;font-size:13px;">'
    )


def _svg_end():
    return "</svg>"


def _svg_line(x1, y1, x2, y2, color="#333", width=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def _svg_circle(cx, cy, r, fill="none", stroke="#333", width=2):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def _svg_polygon(points, fill="none", stroke="#333", width=2):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def _svg_text(x, y, text, color="#e63946", bold=False, size=None):
    weight = ' font-weight="bold"' if bold else ""
    sz = f' font-size="{size}"' if size else ""
    return f'<text x="{x}" y="{y}" fill="{color}"{weight}{sz} text-anchor="middle">{text}</text>'


def _svg_label_known(x, y, text):
    return _svg_text(x, y, text, color="#2a9d8f", bold=True)


def _svg_label_unknown(x, y, text):
    return _svg_text(x, y, text, color="#e63946", bold=True)


def _svg_arc_angle(cx, cy, angle_start_deg, angle_end_deg, radius=20, label=""):
    """Draw a small arc to indicate an angle."""
    a1 = math.radians(angle_start_deg)
    a2 = math.radians(angle_end_deg)
    x1 = cx + radius * math.cos(a1)
    y1 = cy - radius * math.sin(a1)
    x2 = cx + radius * math.cos(a2)
    y2 = cy - radius * math.sin(a2)
    large = 1 if abs(angle_end_deg - angle_start_deg) > 180 else 0
    path = (
        f'<path d="M {x1:.1f} {y1:.1f} A {radius} {radius} 0 {large} 0 {x2:.1f} {y2:.1f}" '
        f'fill="none" stroke="#e63946" stroke-width="1.5"/>'
    )
    if label:
        mid_a = math.radians((angle_start_deg + angle_end_deg) / 2)
        lx = cx + (radius + 12) * math.cos(mid_a)
        ly = cy - (radius + 12) * math.sin(mid_a)
        path += _svg_text(lx, ly, label, color="#e63946", size=11)
    return path


def _svg_right_angle(cx, cy, dir1_deg, dir2_deg, size=12):
    """Draw a small square indicating a right angle."""
    a1 = math.radians(dir1_deg)
    a2 = math.radians(dir2_deg)
    px = cx + size * math.cos(a1)
    py = cy - size * math.sin(a1)
    qx = cx + size * math.cos(a2)
    qy = cy - size * math.sin(a2)
    rx = px + size * math.cos(a2)
    ry = py - size * math.sin(a2)
    return (
        f'<polyline points="{px:.1f},{py:.1f} {rx:.1f},{ry:.1f} {qx:.1f},{qy:.1f}" '
        f'fill="none" stroke="#e63946" stroke-width="1.5"/>'
    )


# ---------------------------------------------------------------------------
# Template functions
# Each returns (question, correct_value, svg, explanation, tip)
# ---------------------------------------------------------------------------

# ============ LEVEL 1 ============

def _t1_pythagoras_hypotenuse():
    """Find hypotenuse given two legs."""
    a = random.randint(3, 12)
    b = random.randint(3, 12)
    c = math.sqrt(a * a + b * b)

    # SVG: right triangle
    ox, oy = 50, 200
    bx, by = ox + a * 12, oy
    tx, ty = ox, oy - b * 12
    svg = _svg_start()
    svg += _svg_polygon([(ox, oy), (bx, by), (tx, ty)], fill="#f0f7ff")
    svg += _svg_right_angle(ox, oy, 0, 90)
    svg += _svg_label_known((ox + bx) / 2, oy + 20, f"{a}")
    svg += _svg_label_known(ox - 20, (oy + ty) / 2, f"{b}")
    svg += _svg_label_unknown((bx + tx) / 2 + 15, (by + ty) / 2, "?")
    svg += _svg_end()

    question = (
        f"Un triangolo rettangolo ha cateti di lunghezza {a} e {b}. "
        f"Quanto misura l'ipotenusa?"
    )
    explanation = (
        f"Applichiamo il Teorema di Pitagora: c = sqrt(a^2 + b^2) = sqrt({a}^2 + {b}^2) "
        f"= sqrt({a*a} + {b*b}) = sqrt({a*a + b*b}) = {_fmt(c)}."
    )
    tip = "Il Teorema di Pitagora si applica solo ai triangoli rettangoli: c^2 = a^2 + b^2."
    return question, c, svg, explanation, tip


def _t1_pythagoras_leg():
    """Find a leg given hypotenuse and the other leg."""
    a = random.randint(3, 12)
    b = random.randint(a + 1, a + 10)
    c = math.sqrt(a * a + b * b)
    # ask for b given a and c
    target = b

    ox, oy = 50, 200
    bx, by = ox + a * 10, oy
    tx, ty = ox, oy - b * 10
    svg = _svg_start()
    svg += _svg_polygon([(ox, oy), (bx, by), (tx, ty)], fill="#f0f7ff")
    svg += _svg_right_angle(ox, oy, 0, 90)
    svg += _svg_label_known((ox + bx) / 2, oy + 20, f"{a}")
    svg += _svg_label_unknown(ox - 20, (oy + ty) / 2, "?")
    svg += _svg_label_known((bx + tx) / 2 + 15, (by + ty) / 2, _fmt(c))
    svg += _svg_end()

    question = (
        f"Un triangolo rettangolo ha un cateto di lunghezza {a} e l'ipotenusa di {_fmt(c)}. "
        f"Quanto misura l'altro cateto?"
    )
    explanation = (
        f"Dal Teorema di Pitagora: b = sqrt(c^2 - a^2) = sqrt({_fmt(c)}^2 - {a}^2) "
        f"= sqrt({_fmt(c*c)} - {a*a}) = sqrt({_fmt(c*c - a*a)}) = {_fmt(target)}."
    )
    tip = "Per trovare un cateto: cateto = sqrt(ipotenusa^2 - altro_cateto^2)."
    return question, target, svg, explanation, tip


def _t1_rectangle_area():
    """Find area of a rectangle given sides."""
    a = random.randint(4, 15)
    b = random.randint(3, 12)
    area = a * b

    ox, oy = 40, 60
    svg = _svg_start()
    svg += _svg_polygon(
        [(ox, oy), (ox + a * 14, oy), (ox + a * 14, oy + b * 14), (ox, oy + b * 14)],
        fill="#f0f7ff"
    )
    svg += _svg_label_known(ox + a * 7, oy - 10, f"{a}")
    svg += _svg_label_known(ox - 18, oy + b * 7, f"{b}")
    svg += _svg_label_unknown(ox + a * 7, oy + b * 7 + 5, "A = ?")
    svg += _svg_end()

    question = f"Un rettangolo ha base {a} cm e altezza {b} cm. Qual e' l'area?"
    explanation = f"Area del rettangolo = base * altezza = {a} * {b} = {area} cm^2."
    tip = "Area del rettangolo = base * altezza. Non confondere con il perimetro = 2*(base + altezza)."
    return question, float(area), svg, explanation, tip


def _t1_circle_area():
    """Find the area of a circle given radius."""
    r = random.randint(2, 10)
    area = math.pi * r * r

    cx, cy = 150, 130
    svg = _svg_start()
    svg += _svg_circle(cx, cy, r * 10)
    svg += _svg_line(cx, cy, cx + r * 10, cy, color="#2a9d8f", width=2)
    svg += _svg_label_known(cx + r * 5, cy - 10, f"r = {r}")
    svg += _svg_label_unknown(cx, cy + r * 10 + 20, "A = ?")
    svg += _svg_end()

    question = f"Un cerchio ha raggio {r} cm. Qual e' l'area? (usa pi greco = 3.14159...)"
    explanation = (
        f"Area del cerchio = pi * r^2 = pi * {r}^2 = pi * {r*r} = {_fmt(area)} cm^2."
    )
    tip = "Area del cerchio = pi * r^2. La circonferenza invece e' 2 * pi * r."
    return question, area, svg, explanation, tip


def _t1_triangle_area():
    """Find area of a triangle given base and height."""
    base = random.randint(4, 16)
    h = random.randint(3, 12)
    area = base * h / 2

    ox, oy = 40, 210
    svg = _svg_start()
    svg += _svg_polygon(
        [(ox, oy), (ox + base * 12, oy), (ox + base * 6, oy - h * 14)],
        fill="#f0f7ff"
    )
    # height dashed line
    svg += f'<line x1="{ox + base * 6}" y1="{oy - h * 14}" x2="{ox + base * 6}" y2="{oy}" stroke="#aaa" stroke-width="1" stroke-dasharray="4,4"/>'
    svg += _svg_label_known(ox + base * 6, oy + 18, f"b = {base}")
    svg += _svg_label_known(ox + base * 6 + 20, (oy + oy - h * 14) / 2, f"h = {h}")
    svg += _svg_label_unknown(ox + base * 4, oy - h * 5, "A = ?")
    svg += _svg_end()

    question = f"Un triangolo ha base {base} cm e altezza {h} cm. Qual e' l'area?"
    explanation = f"Area del triangolo = (base * altezza) / 2 = ({base} * {h}) / 2 = {_fmt(area)} cm^2."
    tip = "Area del triangolo = (b * h) / 2. L'altezza deve essere perpendicolare alla base scelta."
    return question, area, svg, explanation, tip


# ============ LEVEL 2 ============

def _t2_pythagoras_plus_area():
    """Find area of right triangle given hypotenuse and one leg."""
    a = random.randint(3, 10)
    b = random.randint(a + 1, a + 8)
    c = math.sqrt(a * a + b * b)
    area = a * b / 2

    ox, oy = 50, 200
    bx, by = ox + a * 12, oy
    tx, ty = ox, oy - b * 12
    svg = _svg_start()
    svg += _svg_polygon([(ox, oy), (bx, by), (tx, ty)], fill="#f0f7ff")
    svg += _svg_right_angle(ox, oy, 0, 90)
    svg += _svg_label_known((ox + bx) / 2, oy + 20, f"{a}")
    svg += _svg_label_known((bx + tx) / 2 + 15, (by + ty) / 2, _fmt(c))
    svg += _svg_label_unknown(ox + a * 4, oy - b * 4, "A = ?")
    svg += _svg_end()

    question = (
        f"Un triangolo rettangolo ha un cateto di {a} cm e l'ipotenusa di {_fmt(c)} cm. "
        f"Qual e' l'area del triangolo?"
    )
    explanation = (
        f"Passo 1 - Pitagora: l'altro cateto = sqrt({_fmt(c)}^2 - {a}^2) = "
        f"sqrt({_fmt(c*c)} - {a*a}) = sqrt({_fmt(c*c - a*a)}) = {b} cm.\n"
        f"Passo 2 - Area: A = (cateto1 * cateto2) / 2 = ({a} * {b}) / 2 = {_fmt(area)} cm^2."
    )
    tip = "Per l'area di un triangolo rettangolo puoi usare i cateti come base e altezza."
    return question, area, svg, explanation, tip


def _t2_similar_triangles():
    """Find unknown side using triangle similarity."""
    a = random.randint(3, 8)
    b = random.randint(a + 2, a + 8)
    k = random.choice([2, 3, 4])
    a2 = a * k
    b2 = b * k

    ox, oy = 30, 220
    # small triangle
    svg = _svg_start(350, 260)
    p1s = [(ox, oy), (ox + a * 10, oy), (ox + a * 5, oy - b * 8)]
    svg += _svg_polygon(p1s, fill="#f0f7ff")
    svg += _svg_label_known((ox + ox + a * 10) / 2, oy + 18, f"{a}")
    svg += _svg_label_known(ox - 5, (oy + oy - b * 8) / 2, f"{b}")

    # big triangle
    bx = 180
    scale = 5
    p2s = [(bx, oy), (bx + a2 * scale, oy), (bx + a2 * scale // 2, oy - b2 * (scale - 1))]
    svg += _svg_polygon(p2s, fill="#fff3e0")
    svg += _svg_label_known((bx + bx + a2 * scale) / 2, oy + 18, f"{a2}")
    svg += _svg_label_unknown(bx - 10, (oy + oy - b2 * (scale - 1)) / 2, "?")
    svg += _svg_text(100, 20, "Triangoli simili", color="#555", size=14)
    svg += _svg_end()

    question = (
        f"Due triangoli sono simili. Il primo ha lati {a} cm e {b} cm. "
        f"Il secondo ha il lato corrispondente al primo di {a2} cm. "
        f"Quanto misura l'altro lato corrispondente del secondo triangolo?"
    )
    explanation = (
        f"Passo 1 - Rapporto di similitudine: k = {a2}/{a} = {k}.\n"
        f"Passo 2 - Lato incognito: {b} * {k} = {b2} cm."
    )
    tip = "Nei triangoli simili, tutti i lati sono proporzionali con lo stesso rapporto k."
    return question, float(b2), svg, explanation, tip


def _t2_trapezoid_area():
    """Find area of trapezoid given bases and need to find height with Pythagoras."""
    B = random.randint(8, 16)
    b_small = random.randint(3, B - 2)
    leg = random.randint(3, 10)
    diff = B - b_small
    h = math.sqrt(leg * leg - (diff / 2) ** 2) if leg > diff / 2 else None
    # ensure valid geometry
    while h is None or h < 1:
        leg = random.randint(max(3, int(diff / 2) + 1), int(diff / 2) + 10)
        h_sq = leg * leg - (diff / 2) ** 2
        if h_sq > 0:
            h = math.sqrt(h_sq)
        else:
            h = None

    area = (B + b_small) * h / 2

    ox, oy = 30, 200
    svg = _svg_start()
    offset = (B - b_small) * 6
    pts = [
        (ox, oy),
        (ox + B * 12, oy),
        (ox + B * 12 - offset, oy - h * 12),
        (ox + offset, oy - h * 12),
    ]
    svg += _svg_polygon(pts, fill="#f0f7ff")
    svg += _svg_label_known(ox + B * 6, oy + 18, f"B = {B}")
    svg += _svg_label_known((pts[2][0] + pts[3][0]) / 2, pts[2][1] - 15, f"b = {b_small}")
    svg += _svg_label_known(ox - 25, (oy + pts[3][1]) / 2, f"l = {leg}")
    svg += _svg_label_unknown(ox + B * 6, (oy + pts[2][1]) / 2, "A = ?")
    svg += _svg_end()

    question = (
        f"Un trapezio isoscele ha base maggiore {B} cm, base minore {b_small} cm "
        f"e lato obliquo {leg} cm. Qual e' l'area?"
    )
    explanation = (
        f"Passo 1 - Altezza con Pitagora: la differenza delle basi e' ({B} - {b_small}) = {diff} cm, "
        f"meta' = {_fmt(diff/2)} cm. h = sqrt({leg}^2 - {_fmt(diff/2)}^2) = {_fmt(h)} cm.\n"
        f"Passo 2 - Area trapezio: A = (B + b) * h / 2 = ({B} + {b_small}) * {_fmt(h)} / 2 = {_fmt(area)} cm^2."
    )
    tip = "Nel trapezio isoscele, l'altezza si trova con Pitagora sul triangolo rettangolo laterale."
    return question, area, svg, explanation, tip


def _t2_circle_sector_area():
    """Find area of circular sector given radius and angle."""
    r = random.randint(4, 12)
    angle_deg = random.choice([30, 45, 60, 90, 120, 150])
    area = math.pi * r * r * angle_deg / 360

    cx, cy = 150, 140
    a1 = math.radians(0)
    a2 = math.radians(angle_deg)
    x1 = cx + r * 8 * math.cos(a1)
    y1 = cy - r * 8 * math.sin(a1)
    x2 = cx + r * 8 * math.cos(a2)
    y2 = cy - r * 8 * math.sin(a2)
    large_flag = 1 if angle_deg > 180 else 0

    svg = _svg_start()
    svg += (
        f'<path d="M {cx} {cy} L {x1:.1f} {y1:.1f} '
        f'A {r*8} {r*8} 0 {large_flag} 0 {x2:.1f} {y2:.1f} Z" '
        f'fill="#f0f7ff" stroke="#333" stroke-width="2"/>'
    )
    svg += _svg_label_known(cx + r * 4 + 5, cy + 15, f"r = {r}")
    svg += _svg_arc_angle(cx, cy, 0, angle_deg, radius=25, label=f"{angle_deg}")
    svg += _svg_label_unknown(cx - 40, cy - r * 4, "A = ?")
    svg += _svg_end()

    question = (
        f"Un settore circolare ha raggio {r} cm e angolo al centro di {angle_deg} gradi. "
        f"Qual e' l'area del settore?"
    )
    explanation = (
        f"Passo 1 - Formula settore: A = pi * r^2 * angolo / 360.\n"
        f"Passo 2 - Calcolo: A = pi * {r}^2 * {angle_deg} / 360 "
        f"= pi * {r*r} * {angle_deg} / 360 = {_fmt(area)} cm^2."
    )
    tip = "L'area del settore circolare e' la frazione angolo/360 dell'area totale del cerchio."
    return question, area, svg, explanation, tip


def _t2_trig_right_triangle():
    """Find a side of a right triangle using basic trigonometry."""
    angle_deg = random.choice([30, 45, 60])
    hyp = random.randint(5, 15)
    angle_rad = math.radians(angle_deg)
    opp = hyp * math.sin(angle_rad)
    adj = hyp * math.cos(angle_rad)

    # ask for the opposite side
    ox, oy = 50, 210
    bx, by = ox + int(adj * 12), oy
    tx, ty = ox, oy - int(opp * 12)

    svg = _svg_start()
    svg += _svg_polygon([(ox, oy), (bx, by), (tx, ty)], fill="#f0f7ff")
    svg += _svg_right_angle(ox, oy, 0, 90)
    svg += _svg_label_known((bx + tx) / 2 + 15, (by + ty) / 2, f"{hyp}")
    svg += _svg_arc_angle(bx, by, 90 + angle_deg, 180, radius=22, label=f"{angle_deg}")
    svg += _svg_label_unknown(ox - 18, (oy + ty) / 2, "?")
    svg += _svg_end()

    question = (
        f"Un triangolo rettangolo ha ipotenusa {hyp} cm e un angolo acuto di {angle_deg} gradi. "
        f"Quanto misura il cateto opposto all'angolo?"
    )
    explanation = (
        f"Passo 1 - Identifichiamo: sin({angle_deg}) = cateto opposto / ipotenusa.\n"
        f"Passo 2 - cateto opposto = {hyp} * sin({angle_deg}) = {hyp} * {_fmt(math.sin(angle_rad))} "
        f"= {_fmt(opp)} cm."
    )
    tip = "SOH-CAH-TOA: sin = opposto/ipotenusa, cos = adiacente/ipotenusa, tan = opposto/adiacente."
    return question, opp, svg, explanation, tip


def _t2_perimeter_composite():
    """Find perimeter of a figure made of a rectangle plus a semicircle."""
    w = random.randint(4, 10)
    h = random.randint(4, 10)
    # semicircle on top of width
    r = w / 2
    perim = w + 2 * h + math.pi * r

    ox, oy = 60, 220
    rw = w * 14
    rh = h * 14
    svg = _svg_start()
    # rectangle (3 sides)
    svg += _svg_line(ox, oy, ox + rw, oy)
    svg += _svg_line(ox, oy, ox, oy - rh)
    svg += _svg_line(ox + rw, oy, ox + rw, oy - rh)
    # semicircle on top
    scx = ox + rw / 2
    scy = oy - rh
    svg += (
        f'<path d="M {ox} {scy} A {rw/2} {rw/2} 0 0 1 {ox + rw} {scy}" '
        f'fill="none" stroke="#333" stroke-width="2"/>'
    )
    svg += _svg_label_known(ox + rw / 2, oy + 18, f"{w}")
    svg += _svg_label_known(ox - 18, oy - rh / 2, f"{h}")
    svg += _svg_label_unknown(ox + rw + 20, oy - rh / 2, "P = ?")
    svg += _svg_end()

    question = (
        f"Una figura e' formata da un rettangolo di base {w} cm e altezza {h} cm, "
        f"con un semicerchio costruito sulla base superiore. "
        f"Qual e' il perimetro della figura?"
    )
    explanation = (
        f"Passo 1 - Il perimetro include: base inferiore ({w}), due lati verticali (2 * {h}), "
        f"e il semicerchio (pi * r = pi * {_fmt(r)}).\n"
        f"Passo 2 - P = {w} + 2 * {h} + pi * {_fmt(r)} = {_fmt(perim)} cm."
    )
    tip = "Per figure composite, identifica ogni segmento del contorno e somma le lunghezze."
    return question, perim, svg, explanation, tip


# ============ LEVEL 3 ============

def _t3_distance_two_points():
    """Find distance between two points on the Cartesian plane."""
    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)
    x2 = random.randint(-5, 5)
    y2 = random.randint(-5, 5)
    while x1 == x2 and y1 == y2:
        x2 = random.randint(-5, 5)
        y2 = random.randint(-5, 5)
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # SVG with Cartesian grid
    ox, oy = 150, 130  # origin in SVG
    scale = 15
    svg = _svg_start()
    # axes
    svg += _svg_line(20, oy, 280, oy, color="#ccc")
    svg += _svg_line(ox, 10, ox, 240, color="#ccc")
    svg += _svg_text(285, oy + 4, "x", color="#999", size=11)
    svg += _svg_text(ox + 4, 12, "y", color="#999", size=11)
    # points
    px1, py1 = ox + x1 * scale, oy - y1 * scale
    px2, py2 = ox + x2 * scale, oy - y2 * scale
    svg += f'<circle cx="{px1}" cy="{py1}" r="4" fill="#2a9d8f"/>'
    svg += _svg_label_known(px1, py1 - 10, f"A({x1},{y1})")
    svg += f'<circle cx="{px2}" cy="{py2}" r="4" fill="#e63946"/>'
    svg += _svg_label_unknown(px2, py2 - 10, f"B({x2},{y2})")
    svg += f'<line x1="{px1}" y1="{py1}" x2="{px2}" y2="{py2}" stroke="#e63946" stroke-width="2" stroke-dasharray="5,5"/>'
    svg += _svg_label_unknown((px1 + px2) / 2 + 15, (py1 + py2) / 2 + 15, "d = ?")
    svg += _svg_end()

    question = (
        f"Trova la distanza tra i punti A({x1}, {y1}) e B({x2}, {y2}) nel piano cartesiano."
    )
    explanation = (
        f"Formula della distanza: d = sqrt((x2-x1)^2 + (y2-y1)^2) "
        f"= sqrt(({x2}-{x1 if x1 >= 0 else '(' + str(x1) + ')'})^2 + ({y2}-{y1 if y1 >= 0 else '(' + str(y1) + ')'})^2) "
        f"= sqrt({(x2-x1)**2} + {(y2-y1)**2}) = sqrt({(x2-x1)**2 + (y2-y1)**2}) = {_fmt(dist)}."
    )
    tip = "La formula della distanza e' un'applicazione diretta del Teorema di Pitagora nel piano cartesiano."
    return question, dist, svg, explanation, tip


def _t3_midpoint_and_distance():
    """Find midpoint then compute distance from midpoint to a third point."""
    x1 = random.randint(-4, 4)
    y1 = random.randint(-4, 4)
    x2 = random.randint(-4, 4)
    y2 = random.randint(-4, 4)
    while x1 == x2 and y1 == y2:
        x2 = random.randint(-4, 4)
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    x3 = random.randint(-4, 4)
    y3 = random.randint(-4, 4)
    while (x3 == mx and y3 == my):
        x3 = random.randint(-4, 4)
    target = math.sqrt((x3 - mx) ** 2 + (y3 - my) ** 2)

    ox, oy = 150, 130
    scale = 15
    svg = _svg_start()
    svg += _svg_line(20, oy, 280, oy, color="#ccc")
    svg += _svg_line(ox, 10, ox, 240, color="#ccc")
    px1, py1 = ox + x1 * scale, oy - y1 * scale
    px2, py2 = ox + x2 * scale, oy - y2 * scale
    px3, py3 = ox + x3 * scale, oy - y3 * scale
    svg += _svg_line(px1, py1, px2, py2, color="#2a9d8f")
    svg += f'<circle cx="{px1}" cy="{py1}" r="4" fill="#2a9d8f"/>'
    svg += _svg_label_known(px1, py1 - 10, f"A({x1},{y1})")
    svg += f'<circle cx="{px2}" cy="{py2}" r="4" fill="#2a9d8f"/>'
    svg += _svg_label_known(px2, py2 - 10, f"B({x2},{y2})")
    svg += f'<circle cx="{px3}" cy="{py3}" r="4" fill="#e63946"/>'
    svg += _svg_label_unknown(px3, py3 - 10, f"C({x3},{y3})")
    svg += _svg_end()

    question = (
        f"Dati A({x1},{y1}) e B({x2},{y2}), trova il punto medio M di AB. "
        f"Poi calcola la distanza tra M e il punto C({x3},{y3})."
    )
    explanation = (
        f"Passo 1 - Punto medio: M = (({x1}+{x2})/2, ({y1}+{y2})/2) = ({_fmt(mx)}, {_fmt(my)}).\n"
        f"Passo 2 - Distanza MC: d = sqrt(({x3}-{_fmt(mx)})^2 + ({y3}-{_fmt(my)})^2) = {_fmt(target)}."
    )
    tip = "Punto medio M = ((x1+x2)/2, (y1+y2)/2). Combina con la formula della distanza per problemi a due passi."
    return question, target, svg, explanation, tip


def _t3_triangle_area_coordinates():
    """Find area of triangle given three vertices using the coordinate formula."""
    for _attempt in range(200):
        x1, y1 = random.randint(-3, 3), random.randint(-3, 3)
        x2, y2 = random.randint(-3, 3), random.randint(-3, 3)
        x3, y3 = random.randint(-3, 3), random.randint(-3, 3)
        area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
        if area >= 1:
            break
    else:
        x1, y1, x2, y2, x3, y3 = 0, 0, 3, 0, 0, 4
        area = 6.0

    ox, oy = 150, 130
    scale = 18
    svg = _svg_start()
    svg += _svg_line(20, oy, 280, oy, color="#ccc")
    svg += _svg_line(ox, 10, ox, 240, color="#ccc")
    pts_svg = [
        (ox + x1 * scale, oy - y1 * scale),
        (ox + x2 * scale, oy - y2 * scale),
        (ox + x3 * scale, oy - y3 * scale),
    ]
    svg += _svg_polygon(pts_svg, fill="#f0f7ff")
    svg += f'<circle cx="{pts_svg[0][0]}" cy="{pts_svg[0][1]}" r="3" fill="#2a9d8f"/>'
    svg += _svg_label_known(pts_svg[0][0], pts_svg[0][1] - 10, f"A({x1},{y1})")
    svg += f'<circle cx="{pts_svg[1][0]}" cy="{pts_svg[1][1]}" r="3" fill="#2a9d8f"/>'
    svg += _svg_label_known(pts_svg[1][0], pts_svg[1][1] - 10, f"B({x2},{y2})")
    svg += f'<circle cx="{pts_svg[2][0]}" cy="{pts_svg[2][1]}" r="3" fill="#2a9d8f"/>'
    svg += _svg_label_known(pts_svg[2][0], pts_svg[2][1] - 10, f"C({x3},{y3})")
    svg += _svg_label_unknown(
        sum(p[0] for p in pts_svg) / 3,
        sum(p[1] for p in pts_svg) / 3 + 5,
        "A = ?"
    )
    svg += _svg_end()

    question = (
        f"Calcola l'area del triangolo con vertici A({x1},{y1}), B({x2},{y2}) e C({x3},{y3}) "
        f"nel piano cartesiano."
    )
    explanation = (
        f"Formula dell'area con coordinate: A = |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)| / 2\n"
        f"= |{x1}*({y2}-{y3}) + {x2}*({y3}-{y1}) + {x3}*({y1}-{y2})| / 2\n"
        f"= |{x1*(y2-y3)} + {x2*(y3-y1)} + {x3*(y1-y2)}| / 2\n"
        f"= {abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))} / 2 = {_fmt(area)}."
    )
    tip = "La formula di Gauss (o del laccio) permette di calcolare l'area di un poligono dalle coordinate dei vertici."
    return question, area, svg, explanation, tip


def _t3_circle_tangent_length():
    """Find the length of a tangent from an external point to a circle (coordinate + Pythagoras)."""
    cx, cy = 0, 0
    r = random.randint(2, 6)
    px = random.randint(r + 2, r + 8)
    py = random.randint(r + 2, r + 8)
    d = math.sqrt(px * px + py * py)
    tangent = math.sqrt(d * d - r * r)

    svgox, svgoy = 80, 160
    scale = 12
    svg = _svg_start()
    svg += _svg_line(20, svgoy, 280, svgoy, color="#ccc")
    svg += _svg_line(svgox, 10, svgox, 240, color="#ccc")
    svg += _svg_circle(svgox, svgoy, r * scale, fill="#f0f7ff")
    svg += _svg_label_known(svgox + 5, svgoy - r * scale - 8, f"r = {r}")
    ppx, ppy = svgox + px * scale, svgoy - py * scale
    svg += f'<circle cx="{ppx}" cy="{ppy}" r="4" fill="#e63946"/>'
    svg += _svg_label_unknown(ppx + 8, ppy - 10, f"P({px},{py})")
    svg += f'<line x1="{svgox}" y1="{svgoy}" x2="{ppx}" y2="{ppy}" stroke="#aaa" stroke-width="1" stroke-dasharray="4,4"/>'
    svg += _svg_label_unknown(ppx - 30, ppy + 25, "t = ?")
    svg += _svg_end()

    question = (
        f"Un cerchio ha centro nell'origine e raggio {r}. "
        f"Dal punto P({px}, {py}) si traccia una tangente al cerchio. "
        f"Quanto e' lunga la tangente?"
    )
    explanation = (
        f"Passo 1 - Distanza OP: d = sqrt({px}^2 + {py}^2) = sqrt({px*px} + {py*py}) "
        f"= sqrt({px*px + py*py}) = {_fmt(d)}.\n"
        f"Passo 2 - Pitagora (OT perp. tangente): t = sqrt(d^2 - r^2) = sqrt({_fmt(d*d)} - {r*r}) "
        f"= sqrt({_fmt(d*d - r*r)}) = {_fmt(tangent)}."
    )
    tip = "La tangente dal punto esterno e' perpendicolare al raggio nel punto di tangenza: si forma un triangolo rettangolo."
    return question, tangent, svg, explanation, tip


def _t3_line_intersection_area():
    """Find where two lines intersect, then compute the triangle area with the origin."""
    # y = m1*x + q1 and y = m2*x + q2
    m1 = random.choice([1, 2, -1, -2])
    q1 = random.randint(-3, 3)
    m2 = random.choice([v for v in [1, 2, -1, -2, 3] if v != m1])
    q2 = random.randint(-3, 3)
    while m1 == m2:
        m2 = random.choice([1, 2, -1, -2, 3])

    # intersection
    ix = (q2 - q1) / (m1 - m2)
    iy = m1 * ix + q1

    # triangle with origin
    area = abs(ix * iy) / 2  # since one vertex at origin, A = |x*y|/2 for right triangle approx
    # Actually use coordinate formula for O(0,0), A(ix,iy), and we need a third point
    # Let's use the two y-intercepts and find the area of the triangle O, (0, q1), (ix, iy)
    # Simpler: triangle with vertices O(0,0), where line1 crosses x-axis, and intersection point
    x_intercept1 = -q1 / m1 if m1 != 0 else 0
    area = abs(0 * (0 - iy) + x_intercept1 * (iy - 0) + ix * (0 - 0)) / 2
    area = abs(x_intercept1 * iy) / 2

    while area < 0.5:
        q1 = random.randint(1, 4)
        q2 = random.randint(-4, -1)
        ix = (q2 - q1) / (m1 - m2)
        iy = m1 * ix + q1
        x_intercept1 = -q1 / m1 if m1 != 0 else 1
        area = abs(x_intercept1 * iy) / 2

    svgox, svgoy = 150, 130
    scale = 18
    svg = _svg_start()
    svg += _svg_line(20, svgoy, 280, svgoy, color="#ccc")
    svg += _svg_line(svgox, 10, svgox, 240, color="#ccc")
    # draw line 1
    lx1 = svgox + (-5) * scale
    ly1 = svgoy - (m1 * (-5) + q1) * scale
    lx2 = svgox + 5 * scale
    ly2 = svgoy - (m1 * 5 + q1) * scale
    svg += _svg_line(lx1, ly1, lx2, ly2, color="#2a9d8f", width=2)
    # draw line 2
    lx3 = svgox + (-5) * scale
    ly3 = svgoy - (m2 * (-5) + q2) * scale
    lx4 = svgox + 5 * scale
    ly4 = svgoy - (m2 * 5 + q2) * scale
    svg += _svg_line(lx3, ly3, lx4, ly4, color="#e76f51", width=2)
    # intersection point
    pix = svgox + ix * scale
    piy = svgoy - iy * scale
    svg += f'<circle cx="{pix:.1f}" cy="{piy:.1f}" r="4" fill="#e63946"/>'
    svg += _svg_text(15, 20, f"y = {m1}x {'+' if q1 >= 0 else ''}{q1}", color="#2a9d8f", size=11)
    svg += _svg_text(15, 38, f"y = {m2}x {'+' if q2 >= 0 else ''}{q2}", color="#e76f51", size=11)
    svg += _svg_label_unknown(pix + 10, piy - 10, "A = ?")
    svg += _svg_end()

    question = (
        f"Le rette y = {m1}x {'+' if q1 >= 0 else ''}{q1} e y = {m2}x {'+' if q2 >= 0 else ''}{q2} "
        f"si intersecano nel punto P. La retta y = {m1}x {'+' if q1 >= 0 else ''}{q1} interseca l'asse x "
        f"nel punto Q. Calcola l'area del triangolo OPQ (O = origine)."
    )
    explanation = (
        f"Passo 1 - Intersezione P: {m1}x {'+' if q1 >= 0 else ''}{q1} = {m2}x {'+' if q2 >= 0 else ''}{q2} "
        f"=> x = {_fmt(ix)}, y = {_fmt(iy)}, quindi P = ({_fmt(ix)}, {_fmt(iy)}).\n"
        f"Passo 2 - Q (intersezione asse x): y = 0 => x = {_fmt(x_intercept1)}, quindi Q = ({_fmt(x_intercept1)}, 0).\n"
        f"Passo 3 - Area OPQ con formula coordinate: "
        f"A = |x_O(y_Q - y_P) + x_Q(y_P - y_O) + x_P(y_O - y_Q)| / 2 = {_fmt(area)}."
    )
    tip = "Per trovare l'intersezione di due rette, metti a sistema le equazioni. L'area si calcola con la formula di Gauss."
    return question, area, svg, explanation, tip


def _t3_inscribed_square_circle():
    """Find the side of a square inscribed in a circle, combining coordinate and Euclidean geometry."""
    r = random.randint(3, 10)
    side = r * math.sqrt(2)
    area_sq = side * side

    svgox, svgoy = 150, 130
    svg = _svg_start()
    svg += _svg_circle(svgox, svgoy, r * 10, fill="#fff3e0")
    half = r * 10 * math.sqrt(2) / 2
    pts = [
        (svgox - half, svgoy - half),
        (svgox + half, svgoy - half),
        (svgox + half, svgoy + half),
        (svgox - half, svgoy + half),
    ]
    svg += _svg_polygon(pts, fill="#f0f7ff")
    svg += _svg_label_known(svgox, svgoy - r * 10 - 12, f"r = {r}")
    svg += _svg_line(svgox, svgoy, svgox + r * 10, svgoy, color="#2a9d8f", width=1)
    svg += _svg_label_unknown(svgox, svgoy + r * 10 + 20, "lato = ?")
    svg += _svg_end()

    question = (
        f"Un quadrato e' inscritto in un cerchio di raggio {r}. "
        f"Quanto misura il lato del quadrato?"
    )
    explanation = (
        f"Passo 1 - La diagonale del quadrato inscritto coincide col diametro: d = 2r = {2*r}.\n"
        f"Passo 2 - Relazione diagonale-lato: d = l * sqrt(2) => l = d / sqrt(2) = "
        f"{2*r} / sqrt(2) = {2*r} * sqrt(2) / 2 = {r} * sqrt(2) = {_fmt(side)} cm."
    )
    tip = "In un quadrato inscritto in un cerchio, la diagonale = diametro. Relazione: lato = diagonale / sqrt(2)."
    return question, side, svg, explanation, tip


# ============ SOLID GEOMETRY ============

def _t1_cylinder_volume():
    """Volume di un cilindro dato raggio di base e altezza."""
    r = random.randint(2, 10)
    h = random.randint(3, 15)
    volume = math.pi * r * r * h

    cx, cy_top = 150, 50
    svg_rx = r * 8
    svg_ry = 15
    svg_h = h * 10

    svg = _svg_start(300, 280)
    # Top ellipse
    svg += f'<ellipse cx="{cx}" cy="{cy_top}" rx="{svg_rx}" ry="{svg_ry}" fill="#f0f7ff" stroke="#333" stroke-width="2"/>'
    # Side lines
    svg += _svg_line(cx - svg_rx, cy_top, cx - svg_rx, cy_top + svg_h)
    svg += _svg_line(cx + svg_rx, cy_top, cx + svg_rx, cy_top + svg_h)
    # Bottom ellipse
    svg += f'<ellipse cx="{cx}" cy="{cy_top + svg_h}" rx="{svg_rx}" ry="{svg_ry}" fill="none" stroke="#333" stroke-width="2"/>'
    # Labels
    svg += _svg_label_known(cx, cy_top - 20, f"r = {r}")
    svg += _svg_label_known(cx + svg_rx + 20, cy_top + svg_h // 2, f"h = {h}")
    svg += _svg_label_unknown(cx, cy_top + svg_h + 35, "V = ?")
    svg += _svg_end()

    question = (
        f"Un cilindro ha raggio di base {r} cm e altezza {h} cm. "
        f"Qual e' il volume?"
    )
    explanation = (
        f"Volume del cilindro = pi * r^2 * h = pi * {r}^2 * {h} "
        f"= pi * {r * r} * {h} = {_fmt(volume)} cm^3."
    )
    tip = "Volume del cilindro: V = pi * r^2 * h, cioe' area di base per altezza."
    return question, volume, svg, explanation, tip


def _t1_rectangular_prism_volume():
    """Volume di un parallelepipedo rettangolo."""
    l = random.randint(3, 12)
    w = random.randint(2, 10)
    h = random.randint(2, 10)
    volume = l * w * h

    ox, oy = 60, 180
    sl = l * 10
    sw = w * 6
    sh = h * 10
    dx, dy = int(sw * 0.7), int(sw * 0.5)

    svg = _svg_start(300, 280)
    # Front face
    svg += _svg_polygon([(ox, oy), (ox + sl, oy), (ox + sl, oy - sh), (ox, oy - sh)], fill="#f0f7ff")
    # Top face
    svg += _svg_polygon([(ox, oy - sh), (ox + sl, oy - sh), (ox + sl + dx, oy - sh - dy), (ox + dx, oy - sh - dy)], fill="#dbe9f7")
    # Right face
    svg += _svg_polygon([(ox + sl, oy), (ox + sl + dx, oy - dy), (ox + sl + dx, oy - sh - dy), (ox + sl, oy - sh)], fill="#c8ddf0")
    # Labels
    svg += _svg_label_known(ox + sl // 2, oy + 18, f"lunghezza {l}")
    svg += _svg_label_known(ox - 25, oy - sh // 2, f"altezza {h}")
    svg += _svg_label_known(ox + sl + dx // 2 + 15, oy - dy // 2 + 5, f"larghezza {w}")
    svg += _svg_label_unknown(ox + sl // 2, oy - sh // 2, "V = ?")
    svg += _svg_end()

    question = (
        f"Un parallelepipedo rettangolo ha lunghezza {l} cm, "
        f"larghezza {w} cm e altezza {h} cm. Qual e' il volume?"
    )
    explanation = (
        f"Volume = lunghezza * larghezza * altezza = {l} * {w} * {h} = {volume} cm^3."
    )
    tip = "Volume del parallelepipedo: V = l * w * h, prodotto delle tre dimensioni."
    return question, float(volume), svg, explanation, tip


def _t2_cone_volume():
    """Volume di un cono dato raggio di base e altezza."""
    r = random.randint(2, 10)
    h = random.randint(4, 15)
    volume = math.pi * r * r * h / 3

    cx, cy_apex = 150, 30
    svg_rx = r * 8
    svg_ry = 15
    svg_h = h * 10
    base_cy = cy_apex + svg_h

    svg = _svg_start(300, 280)
    # Cone sides
    svg += _svg_line(cx, cy_apex, cx - svg_rx, base_cy)
    svg += _svg_line(cx, cy_apex, cx + svg_rx, base_cy)
    # Base ellipse
    svg += f'<ellipse cx="{cx}" cy="{base_cy}" rx="{svg_rx}" ry="{svg_ry}" fill="#f0f7ff" stroke="#333" stroke-width="2"/>'
    # Height dashed line
    svg += f'<line x1="{cx}" y1="{cy_apex}" x2="{cx}" y2="{base_cy}" stroke="#aaa" stroke-width="1" stroke-dasharray="4,4"/>'
    # Labels
    svg += _svg_label_known(cx + svg_rx // 2 + 10, base_cy + 5, f"base {r}")
    svg += _svg_label_known(cx + 15, cy_apex + svg_h // 2, f"altezza {h}")
    svg += _svg_label_unknown(cx - svg_rx - 20, base_cy - svg_h // 2, "V = ?")
    svg += _svg_end()

    question = (
        f"Un cono ha raggio di base {r} cm e altezza {h} cm. "
        f"Qual e' il volume?"
    )
    explanation = (
        f"Volume del cono = pi * r^2 * h / 3 = pi * {r}^2 * {h} / 3 "
        f"= pi * {r * r} * {h} / 3 = {_fmt(volume)} cm^3."
    )
    tip = "Volume del cono: V = pi * r^2 * h / 3, cioe' un terzo del cilindro con stessa base e altezza."
    return question, volume, svg, explanation, tip


def _t2_sphere_volume():
    """Volume di una sfera dato il diametro."""
    d = random.randint(4, 20)
    r = d / 2
    volume = 4 * math.pi * r ** 3 / 3

    cx, cy = 150, 130
    svg_r = int(d * 4)

    svg = _svg_start()
    svg += _svg_circle(cx, cy, svg_r, fill="#f0f7ff")
    # Diameter line
    svg += _svg_line(cx - svg_r, cy, cx + svg_r, cy, color="#2a9d8f", width=2)
    svg += _svg_label_known(cx, cy + svg_r + 20, f"diametro {d}")
    svg += _svg_label_unknown(cx, cy - svg_r - 10, "V = ?")
    svg += _svg_end()

    question = (
        f"Una sfera ha diametro {d} cm. Qual e' il volume?"
    )
    explanation = (
        f"Raggio = diametro / 2 = {d} / 2 = {_fmt(r)} cm. "
        f"Volume = 4/3 * pi * r^3 = 4/3 * pi * {_fmt(r)}^3 "
        f"= 4/3 * pi * {_fmt(r**3)} = {_fmt(volume)} cm^3."
    )
    tip = "Volume della sfera: V = 4/3 * pi * r^3. Ricorda di dimezzare il diametro per ottenere il raggio."
    return question, volume, svg, explanation, tip


def _t2_pyramid_volume():
    """Volume di una piramide a base quadrata."""
    l = random.randint(3, 12)
    h = random.randint(4, 15)
    volume = l * l * h / 3

    cx, cy_apex = 150, 30
    base_cy = 200
    half = l * 6
    dx, dy = int(half * 0.6), int(half * 0.35)

    svg = _svg_start(300, 260)
    # Base (parallelogram for 3D effect)
    base_pts = [
        (cx - half, base_cy),
        (cx + half, base_cy),
        (cx + half + dx, base_cy - dy),
        (cx - half + dx, base_cy - dy),
    ]
    svg += _svg_polygon(base_pts, fill="#f0f7ff")
    # Edges to apex
    svg += _svg_line(cx - half, base_cy, cx, cy_apex)
    svg += _svg_line(cx + half, base_cy, cx, cy_apex)
    svg += _svg_line(cx + half + dx, base_cy - dy, cx, cy_apex)
    svg += f'<line x1="{cx - half + dx}" y1="{base_cy - dy}" x2="{cx}" y2="{cy_apex}" stroke="#333" stroke-width="1" stroke-dasharray="4,4"/>'
    # Height dashed line
    svg += f'<line x1="{cx}" y1="{cy_apex}" x2="{cx}" y2="{base_cy}" stroke="#aaa" stroke-width="1" stroke-dasharray="4,4"/>'
    # Labels
    svg += _svg_label_known(cx, base_cy + 18, f"lato di base {l}")
    svg += _svg_label_known(cx + 15, (cy_apex + base_cy) // 2, f"altezza {h}")
    svg += _svg_label_unknown(cx - half - 25, (cy_apex + base_cy) // 2, "V = ?")
    svg += _svg_end()

    question = (
        f"Una piramide a base quadrata ha lato di base {l} cm e altezza {h} cm. "
        f"Qual e' il volume?"
    )
    explanation = (
        f"Volume della piramide = l^2 * h / 3 = {l}^2 * {h} / 3 "
        f"= {l * l} * {h} / 3 = {_fmt(volume)} cm^3."
    )
    tip = "Volume della piramide: V = area_base * h / 3. Per base quadrata: V = l^2 * h / 3."
    return question, volume, svg, explanation, tip


def _t3_composite_cylinder_cone():
    """Volume di una figura composta cilindro + cono con stessa base."""
    r = random.randint(2, 8)
    h_cyl = random.randint(4, 12)
    h_cone = random.randint(3, 10)
    v_cyl = math.pi * r * r * h_cyl
    v_cone = math.pi * r * r * h_cone / 3
    volume = v_cyl + v_cone

    cx = 150
    svg_rx = r * 8
    svg_ry = 15
    cy_top = 30
    svg_h_cone = h_cone * 8
    svg_h_cyl = h_cyl * 8
    cy_cone_base = cy_top + svg_h_cone
    cy_cyl_bottom = cy_cone_base + svg_h_cyl

    svg = _svg_start(300, 300)
    # Cone apex
    svg += _svg_line(cx, cy_top, cx - svg_rx, cy_cone_base)
    svg += _svg_line(cx, cy_top, cx + svg_rx, cy_cone_base)
    # Junction ellipse (cone base / cylinder top)
    svg += f'<ellipse cx="{cx}" cy="{cy_cone_base}" rx="{svg_rx}" ry="{svg_ry}" fill="none" stroke="#333" stroke-width="2"/>'
    # Cylinder sides
    svg += _svg_line(cx - svg_rx, cy_cone_base, cx - svg_rx, cy_cyl_bottom)
    svg += _svg_line(cx + svg_rx, cy_cone_base, cx + svg_rx, cy_cyl_bottom)
    # Bottom ellipse
    svg += f'<ellipse cx="{cx}" cy="{cy_cyl_bottom}" rx="{svg_rx}" ry="{svg_ry}" fill="#f0f7ff" stroke="#333" stroke-width="2"/>'
    # Height lines
    svg += f'<line x1="{cx}" y1="{cy_top}" x2="{cx}" y2="{cy_cone_base}" stroke="#aaa" stroke-width="1" stroke-dasharray="4,4"/>'
    # Labels
    svg += _svg_label_known(cx + svg_rx + 15, cy_cone_base - svg_h_cone // 2, f"altezza {h_cone}")
    svg += _svg_label_known(cx + svg_rx + 15, cy_cone_base + svg_h_cyl // 2, f"altezza {h_cyl}")
    svg += _svg_label_known(cx, cy_cyl_bottom + 25, f"(raggio {r} cm)")
    svg += _svg_label_unknown(cx - svg_rx - 25, cy_cone_base, "V = ?")
    svg += _svg_end()

    question = (
        f"Una figura e' composta da un cilindro (raggio {r} cm, "
        f"altezza {h_cyl} cm) sormontato da un cono con la stessa base e "
        f"altezza {h_cone} cm. Qual e' il volume totale?"
    )
    explanation = (
        f"V_cilindro = pi * {r}^2 * {h_cyl} = {_fmt(v_cyl)} cm^3. "
        f"V_cono = pi * {r}^2 * {h_cone} / 3 = {_fmt(v_cone)} cm^3. "
        f"V_totale = {_fmt(v_cyl)} + {_fmt(v_cone)} = {_fmt(volume)} cm^3."
    )
    tip = "Per figure composte, calcola il volume di ogni solido separatamente e poi somma."
    return question, volume, svg, explanation, tip


def _t3_sphere_inscribed_in_cylinder():
    """Volume residuo: cilindro meno sfera inscritta."""
    r = random.randint(2, 10)
    h = 2 * r
    v_cyl = math.pi * r * r * h
    v_sphere = 4 * math.pi * r ** 3 / 3
    volume = v_cyl - v_sphere

    cx, cy_top = 150, 40
    svg_r = r * 8
    svg_ry = 15
    svg_h = h * 8

    svg = _svg_start(300, 280)
    # Cylinder top ellipse
    svg += f'<ellipse cx="{cx}" cy="{cy_top}" rx="{svg_r}" ry="{svg_ry}" fill="#f0f7ff" stroke="#333" stroke-width="2"/>'
    # Cylinder sides
    svg += _svg_line(cx - svg_r, cy_top, cx - svg_r, cy_top + svg_h)
    svg += _svg_line(cx + svg_r, cy_top, cx + svg_r, cy_top + svg_h)
    # Cylinder bottom ellipse
    svg += f'<ellipse cx="{cx}" cy="{cy_top + svg_h}" rx="{svg_r}" ry="{svg_ry}" fill="none" stroke="#333" stroke-width="2"/>'
    # Inscribed sphere (circle)
    svg += _svg_circle(cx, cy_top + svg_h // 2, svg_r, fill="none", stroke="#e63946", width=2)
    # Labels
    svg += _svg_label_known(cx, cy_top - 20, f"raggio {r} cm")
    svg += _svg_label_unknown(cx + svg_r + 25, cy_top + svg_h // 2, "V = ?")
    svg += _svg_end()

    question = (
        f"Una sfera di raggio {r} cm e' inscritta in un cilindro avente lo stesso raggio "
        f"e altezza uguale al diametro della sfera. "
        f"Qual e' il volume dello spazio tra il cilindro e la sfera?"
    )
    explanation = (
        f"Il cilindro ha r = {r} e h = 2r = {h}. "
        f"V_cilindro = pi * {r}^2 * {h} = {_fmt(v_cyl)} cm^3. "
        f"V_sfera = 4/3 * pi * {r}^3 = {_fmt(v_sphere)} cm^3. "
        f"V_residuo = {_fmt(v_cyl)} - {_fmt(v_sphere)} = {_fmt(volume)} cm^3."
    )
    tip = "La sfera inscritta nel cilindro ha h = 2r. Il volume residuo e' V_cilindro - V_sfera."
    return question, volume, svg, explanation, tip


# ============ CIRCLE ADVANCED ============

def _t2_inscribed_angle():
    """Angolo inscritto: dato l'angolo al centro, trovare l'angolo inscritto (o viceversa)."""
    r = 80  # SVG radius
    cx, cy = 150, 130  # center in SVG coords
    central_angle = random.choice(range(40, 161, 10))  # degrees
    inscribed_angle = central_angle / 2

    # Decide direction: given central, ask inscribed (or vice versa)
    ask_inscribed = random.choice([True, False])

    # Place points A, B, C on the circle
    # A and B define the arc subtending the central angle
    start_deg = random.randint(0, 360)
    a_deg = start_deg
    b_deg = start_deg + central_angle

    # C is on the major arc (opposite side from center angle)
    c_deg = start_deg + 180 + central_angle / 2  # on the far arc

    def point_on_circle(angle_deg):
        rad = math.radians(angle_deg)
        return cx + r * math.cos(rad), cy - r * math.sin(rad)

    ax, ay = point_on_circle(a_deg)
    bx, by = point_on_circle(b_deg)
    cxx, cyy = point_on_circle(c_deg)

    svg = _svg_start()
    svg += _svg_circle(cx, cy, r, fill="#f0f7ff")
    # Center
    svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>'
    svg += _svg_text(cx + 8, cy - 8, "O", color="#333", bold=True, size=12)
    # Points on circle
    svg += f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="3" fill="#2a9d8f"/>'
    svg += _svg_text(ax + 10, ay - 8, "A", color="#2a9d8f", bold=True, size=12)
    svg += f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3" fill="#2a9d8f"/>'
    svg += _svg_text(bx + 10, by - 8, "B", color="#2a9d8f", bold=True, size=12)
    svg += f'<circle cx="{cxx:.1f}" cy="{cyy:.1f}" r="3" fill="#e63946"/>'
    svg += _svg_text(cxx + 10, cyy - 8, "C", color="#e63946", bold=True, size=12)
    # Lines: OA, OB (central angle)
    svg += _svg_line(cx, cy, ax, ay, color="#2a9d8f", width=1)
    svg += _svg_line(cx, cy, bx, by, color="#2a9d8f", width=1)
    # Lines: CA, CB (inscribed angle)
    svg += _svg_line(cxx, cyy, ax, ay, color="#e63946", width=1)
    svg += _svg_line(cxx, cyy, bx, by, color="#e63946", width=1)

    if ask_inscribed:
        # Given central angle, ask for inscribed
        svg += _svg_arc_angle(cx, cy, a_deg, b_deg, radius=22, label=f"{central_angle}\u00b0")
        svg += _svg_label_unknown(cxx - 15, cyy + 20, "? \u00b0")
        question = (
            f"In un cerchio con centro O, l'angolo al centro AOB misura {central_angle}\u00b0. "
            f"Quanto misura l'angolo inscritto ACB che sottende lo stesso arco?"
        )
        correct_value = inscribed_angle
    else:
        # Given inscribed angle, ask for central
        svg += _svg_label_known(cxx - 15, cyy + 20, f"{_fmt(inscribed_angle)}\u00b0")
        svg += _svg_label_unknown(cx - 15, cy + 25, "? \u00b0")
        question = (
            f"In un cerchio con centro O, l'angolo inscritto ACB misura {_fmt(inscribed_angle)}\u00b0. "
            f"Quanto misura l'angolo al centro AOB che sottende lo stesso arco?"
        )
        correct_value = float(central_angle)

    svg += _svg_end()

    explanation = (
        f"Per il teorema dell'angolo inscritto, l'angolo inscritto e' la meta' dell'angolo al centro "
        f"che sottende lo stesso arco. Angolo al centro = {central_angle}\u00b0, "
        f"angolo inscritto = {central_angle}\u00b0 / 2 = {_fmt(inscribed_angle)}\u00b0."
    )
    tip = "Teorema dell'angolo inscritto: l'angolo inscritto e' sempre la meta' dell'angolo al centro che sottende lo stesso arco."
    return question, correct_value, svg, explanation, tip


def _t2_chord_distance():
    """Distanza della corda dal centro del cerchio."""
    # Use Pythagorean triples for clean results
    triples = [
        (5, 6, 4),    # r=5, l=6 (half=3), d=4
        (5, 8, 3),    # r=5, l=8 (half=4), d=3
        (10, 12, 8),  # r=10, l=12 (half=6), d=8
        (10, 16, 6),  # r=10, l=16 (half=8), d=6
        (13, 10, 12), # r=13, l=10 (half=5), d=12
        (13, 24, 5),  # r=13, l=24 (half=12), d=5
        (15, 18, 12), # r=15, l=18 (half=9), d=12
        (17, 16, 15), # r=17, l=16 (half=8), d=15
        (25, 14, 24), # r=25, l=14 (half=7), d=24
        (20, 24, 16), # r=20, l=24 (half=12), d=16
    ]
    r_val, l_val, d_val = random.choice(triples)

    cx, cy = 150, 130
    svg_r = 80  # SVG circle radius

    # Chord drawn horizontally centered
    half_l_svg = svg_r * (l_val / 2) / r_val
    d_svg = svg_r * d_val / r_val

    chord_y = cy + d_svg  # chord below center
    chord_x1 = cx - half_l_svg
    chord_x2 = cx + half_l_svg

    svg = _svg_start()
    svg += _svg_circle(cx, cy, svg_r, fill="#f0f7ff")
    # Center
    svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>'
    svg += _svg_text(cx + 10, cy - 5, "O", color="#333", bold=True, size=12)
    # Chord
    svg += _svg_line(chord_x1, chord_y, chord_x2, chord_y, color="#2a9d8f", width=2)
    svg += _svg_label_known(cx, chord_y + 18, f"l = {l_val}")
    # Perpendicular from center to chord
    svg += f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{chord_y}" stroke="#e63946" stroke-width="1.5" stroke-dasharray="4,4"/>'
    # Right angle marker at foot of perpendicular
    svg += _svg_right_angle(cx, chord_y, 0, 90)
    # Radius to one end of chord
    svg += _svg_line(cx, cy, chord_x2, chord_y, color="#aaa", width=1)
    svg += _svg_label_known(cx + 35, cy - 15, f"r = {r_val}")
    # Unknown distance
    svg += _svg_label_unknown(cx + 12, (cy + chord_y) / 2, "d = ?")
    svg += _svg_end()

    question = (
        f"Un cerchio ha raggio {r_val} cm. Una corda misura {l_val} cm. "
        f"Qual e' la distanza della corda dal centro del cerchio?"
    )
    explanation = (
        f"La perpendicolare dal centro alla corda la divide a meta'. "
        f"Si forma un triangolo rettangolo con ipotenusa r = {r_val} e un cateto = l/2 = {l_val}/2 = {l_val // 2}. "
        f"La distanza del centro dalla corda si calcola col teorema di Pitagora: "
        f"d = sqrt(r^2 - (l/2)^2) = sqrt({r_val}^2 - {l_val // 2}^2) "
        f"= sqrt({r_val**2} - {(l_val // 2)**2}) = sqrt({r_val**2 - (l_val // 2)**2}) = {d_val} cm."
    )
    tip = "Teorema corda-distanza: la perpendicolare dal centro alla corda la divide a meta', formando un triangolo rettangolo."
    return question, float(d_val), svg, explanation, tip


def _t3_arc_length():
    """Lunghezza dell'arco di cerchio dato raggio e angolo al centro."""
    # Use values giving clean multiples of pi
    configs = [
        (6, 60, 2),      # L = 2pi*6*60/360 = 2pi
        (6, 120, 4),     # L = 2pi*6*120/360 = 4pi
        (9, 40, 2),      # L = 2pi*9*40/360 = 2pi
        (9, 120, 6),     # L = 2pi*9*120/360 = 6pi
        (3, 60, 1),      # L = 2pi*3*60/360 = pi
        (3, 120, 2),     # L = 2pi*3*120/360 = 2pi
        (12, 90, 6),     # L = 2pi*12*90/360 = 6pi
        (12, 60, 4),     # L = 2pi*12*60/360 = 4pi
        (18, 60, 6),     # L = 2pi*18*60/360 = 6pi
        (15, 72, 6),     # L = 2pi*15*72/360 = 6pi
    ]
    r_val, alpha_deg, pi_mult = random.choice(configs)
    arc_length = 2 * math.pi * r_val * alpha_deg / 360  # = pi_mult * pi

    cx, cy = 150, 130
    svg_r = 80

    # Draw the arc
    a1_rad = math.radians(0)
    a2_rad = math.radians(alpha_deg)
    x1 = cx + svg_r * math.cos(a1_rad)
    y1 = cy - svg_r * math.sin(a1_rad)
    x2 = cx + svg_r * math.cos(a2_rad)
    y2 = cy - svg_r * math.sin(a2_rad)
    large_flag = 1 if alpha_deg > 180 else 0

    svg = _svg_start()
    svg += _svg_circle(cx, cy, svg_r, fill="#f0f7ff")
    # Highlight the arc
    svg += (
        f'<path d="M {x1:.1f} {y1:.1f} A {svg_r} {svg_r} 0 {large_flag} 0 {x2:.1f} {y2:.1f}" '
        f'fill="none" stroke="#e63946" stroke-width="4"/>'
    )
    # Center
    svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>'
    svg += _svg_text(cx + 10, cy + 15, "O", color="#333", bold=True, size=12)
    # Radii
    svg += _svg_line(cx, cy, x1, y1, color="#2a9d8f", width=1)
    svg += _svg_line(cx, cy, x2, y2, color="#2a9d8f", width=1)
    # Angle arc
    svg += _svg_arc_angle(cx, cy, 0, alpha_deg, radius=25, label=f"{alpha_deg}\u00b0")
    # Labels
    svg += _svg_label_known(cx + svg_r / 2 + 5, cy + 15, f"r = {r_val}")
    # Arc length label at midpoint of arc
    mid_angle = math.radians(alpha_deg / 2)
    lx = cx + (svg_r + 18) * math.cos(mid_angle)
    ly = cy - (svg_r + 18) * math.sin(mid_angle)
    svg += _svg_label_unknown(lx, ly, "L = ?")
    svg += _svg_end()

    question = (
        f"Un cerchio ha raggio {r_val} cm. Calcola la lunghezza dell'arco "
        f"sotteso da un angolo al centro di {alpha_deg}\u00b0."
    )
    explanation = (
        f"La lunghezza dell'arco e' la frazione dell'angolo sulla circonferenza totale: "
        f"L = 2*pi*r * alpha/360 = 2*pi*{r_val} * {alpha_deg}/360 "
        f"= {_fmt(2 * r_val)}*pi * {alpha_deg}/360 = {pi_mult}*pi = {_fmt(arc_length)} cm."
    )
    tip = "Lunghezza arco: L = 2*pi*r * angolo/360. E' la proporzione tra angolo e giro completo applicata alla circonferenza."
    return question, arc_length, svg, explanation, tip


def _t3_power_of_point():
    """Potenza di un punto: due secanti da un punto esterno."""
    # PA * PB = PC * PD, all integers
    configs = [
        (3, 8, 4, 6),    # 3*8=24, 4*6=24
        (2, 12, 3, 8),   # 2*12=24, 3*8=24
        (4, 9, 6, 6),    # 4*9=36, 6*6=36
        (2, 18, 4, 9),   # 2*18=36, 4*9=36
        (3, 12, 4, 9),   # 3*12=36, 4*9=36
        (5, 8, 4, 10),   # 5*8=40, 4*10=40
        (2, 15, 5, 6),   # 2*15=30, 5*6=30
        (3, 10, 5, 6),   # 3*10=30, 5*6=30
        (4, 12, 6, 8),   # 4*12=48, 6*8=48
        (6, 8, 4, 12),   # 6*8=48, 4*12=48
    ]
    pa, pb, pc, pd = random.choice(configs)

    # SVG layout: circle in center, point P to the left
    cx, cy = 180, 130
    svg_r = 55

    # P is external, to the left
    px, py = 40, 130

    # First secant goes through circle: segments PA and PB from P
    # Second secant: segments PC and PD from P
    # Position lines at slight angles

    svg = _svg_start()
    svg += _svg_circle(cx, cy, svg_r, fill="#f0f7ff")
    # Point P
    svg += f'<circle cx="{px}" cy="{py}" r="4" fill="#e63946"/>'
    svg += _svg_text(px - 12, py + 4, "P", color="#e63946", bold=True, size=13)

    # First secant (roughly horizontal)
    # A is closer to P, B is farther
    scale1 = (cx + svg_r - px) / pb  # B near far edge of circle
    ax_svg = px + pa * scale1
    ay_svg = py - pa * scale1 * math.sin(0.15)
    bx_svg = px + pb * scale1
    by_svg = py - pb * scale1 * math.sin(0.15)

    svg += _svg_line(px, py, bx_svg, by_svg, color="#2a9d8f", width=1.5)
    svg += f'<circle cx="{ax_svg:.1f}" cy="{ay_svg:.1f}" r="3" fill="#2a9d8f"/>'
    svg += _svg_text(ax_svg, ay_svg - 12, "A", color="#2a9d8f", bold=True, size=12)
    svg += f'<circle cx="{bx_svg:.1f}" cy="{by_svg:.1f}" r="3" fill="#2a9d8f"/>'
    svg += _svg_text(bx_svg + 8, by_svg - 8, "B", color="#2a9d8f", bold=True, size=12)

    # Second secant (angled downward)
    scale2 = (cx + svg_r - px) / pd
    angle2 = -0.25
    cx_svg = px + pc * scale2 * math.cos(angle2)
    cy_svg = py - pc * scale2 * math.sin(angle2)
    dx_svg = px + pd * scale2 * math.cos(angle2)
    dy_svg = py - pd * scale2 * math.sin(angle2)

    svg += _svg_line(px, py, dx_svg, dy_svg, color="#e76f51", width=1.5)
    svg += f'<circle cx="{cx_svg:.1f}" cy="{cy_svg:.1f}" r="3" fill="#e76f51"/>'
    svg += _svg_text(cx_svg, cy_svg + 18, "C", color="#e76f51", bold=True, size=12)
    svg += f'<circle cx="{dx_svg:.1f}" cy="{dy_svg:.1f}" r="3" fill="#e76f51"/>'
    svg += _svg_text(dx_svg + 8, dy_svg + 15, "D", color="#e76f51", bold=True, size=12)

    # Labels for known segments
    svg += _svg_label_known((px + ax_svg) / 2, ay_svg - 18, f"PA={pa}")
    svg += _svg_label_known((ax_svg + bx_svg) / 2, by_svg - 18, f"PB={pb}")
    svg += _svg_label_known((px + cx_svg) / 2, cy_svg + 22, f"PC={pc}")
    svg += _svg_label_unknown((cx_svg + dx_svg) / 2, dy_svg + 22, f"PD=?")
    svg += _svg_end()

    question = (
        f"Da un punto P esterno a un cerchio si tracciano due secanti. "
        f"La prima secante interseca il cerchio nei punti A e B con PA = {pa} e PB = {pb}. "
        f"La seconda secante interseca il cerchio nei punti C e D con PC = {pc}. "
        f"Quanto vale PD?"
    )
    explanation = (
        f"Per il teorema della potenza di un punto: PA * PB = PC * PD. "
        f"Quindi {pa} * {pb} = {pc} * PD, cioe' {pa * pb} = {pc} * PD. "
        f"PD = {pa * pb} / {pc} = {pd}."
    )
    tip = "Teorema della potenza di un punto: per due secanti dallo stesso punto esterno, PA * PB = PC * PD."
    return question, float(pd), svg, explanation, tip


# ---------------------------------------------------------------------------
# SVG helper for coordinate-plane based transformations
# ---------------------------------------------------------------------------

def _svg_coordinate_plane(width=300, height=300, scale=15, origin=None):
    """Return SVG header with coordinate axes drawn.

    Returns (svg_string, ox, oy, scale) where ox/oy is the pixel position
    of the mathematical origin.
    """
    ox = width // 2 if origin is None else origin[0]
    oy = height // 2 if origin is None else origin[1]
    svg = _svg_start(width, height)
    # axes
    svg += _svg_line(10, oy, width - 10, oy, color="#ccc", width=1)
    svg += _svg_line(ox, 10, ox, height - 10, color="#ccc", width=1)
    # axis labels
    svg += _svg_text(width - 12, oy - 6, "x", color="#999", size=11)
    svg += _svg_text(ox + 8, 14, "y", color="#999", size=11)
    return svg, ox, oy, scale


def _svg_point(ox, oy, scale, x, y, label, color="#2a9d8f", r=4):
    """Draw a point on the coordinate plane."""
    px = ox + x * scale
    py = oy - y * scale
    svg = f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{color}"/>'
    svg += _svg_text(px + 10, py - 8, label, color=color, bold=True, size=11)
    return svg


def _svg_dashed_line(x1, y1, x2, y2, color="#aaa", width=1.5):
    """Draw a dashed line."""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" stroke-dasharray="5,4"/>'
    )


def _svg_arrow(x1, y1, x2, y2, color="#e76f51", width=2):
    """Draw a line with an arrowhead."""
    svg = f'<defs><marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{color}"/></marker></defs>'
    svg += (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" marker-end="url(#arrowhead)"/>'
    )
    return svg


# ---------------------------------------------------------------------------
# Transformation templates
# ---------------------------------------------------------------------------

# ============ LEVEL 1 — Transformations ============

def _t1_axial_symmetry():
    """Reflect a point across the x- or y-axis."""
    a = random.choice([v for v in range(-8, 9) if v != 0])
    b = random.choice([v for v in range(-8, 9) if v != 0])
    axis = random.choice(["x", "y"])

    if axis == "x":
        img_x, img_y = a, -b
        axis_name = "asse x"
        ask_coord = "y"
        correct_value = float(img_y)
    else:
        img_x, img_y = -a, b
        axis_name = "asse y"
        ask_coord = "x"
        correct_value = float(img_x)

    scale = 15
    svg, ox, oy, sc = _svg_coordinate_plane(300, 300, scale)
    svg += _svg_point(ox, oy, sc, a, b, f"P({a},{b})", color="#2a9d8f")
    svg += _svg_point(ox, oy, sc, img_x, img_y, f"P'({img_x},{img_y})", color="#e63946")
    # dashed reflection line between original and image
    px1, py1 = ox + a * sc, oy - b * sc
    px2, py2 = ox + img_x * sc, oy - img_y * sc
    svg += _svg_dashed_line(px1, py1, px2, py2, color="#e63946")
    # highlight the reflection axis
    if axis == "x":
        svg += _svg_line(10, oy, 290, oy, color="#e76f51", width=2)
    else:
        svg += _svg_line(ox, 10, ox, 290, color="#e76f51", width=2)
    svg += _svg_end()

    question = (
        f"Il punto P({a}, {b}) viene riflesso rispetto all'{axis_name}. "
        f"Qual e' la coordinata {ask_coord} del punto immagine P'?"
    )
    explanation = (
        f"Riflessione rispetto all'{axis_name}: "
    )
    if axis == "x":
        explanation += (
            f"(x, y) -> (x, -y). Quindi P'({a}, {-b}). "
            f"La coordinata y del punto immagine e' {-b}."
        )
    else:
        explanation += (
            f"(x, y) -> (-x, y). Quindi P'({-a}, {b}). "
            f"La coordinata x del punto immagine e' {-a}."
        )
    tip = "Riflessione rispetto all'asse x: cambia segno a y. Rispetto all'asse y: cambia segno a x."
    return question, correct_value, svg, explanation, tip


def _t1_translation():
    """Translate a point by a vector and ask for one coordinate of the image."""
    a = random.randint(-6, 6)
    b = random.randint(-6, 6)
    h = random.choice([v for v in range(-5, 6) if v != 0])
    k = random.choice([v for v in range(-5, 6) if v != 0])
    img_x = a + h
    img_y = b + k
    ask = random.choice(["x", "y"])
    correct_value = float(img_x) if ask == "x" else float(img_y)

    scale = 15
    svg, ox, oy, sc = _svg_coordinate_plane(300, 300, scale)
    svg += _svg_point(ox, oy, sc, a, b, f"P({a},{b})", color="#2a9d8f")
    svg += _svg_point(ox, oy, sc, img_x, img_y, f"P'({img_x},{img_y})", color="#e63946")
    # arrow showing translation
    px1, py1 = ox + a * sc, oy - b * sc
    px2, py2 = ox + img_x * sc, oy - img_y * sc
    svg += _svg_arrow(px1, py1, px2, py2, color="#e76f51")
    svg += _svg_text(150, 290, f"vettore ({h}, {k})", color="#555", size=12)
    svg += _svg_end()

    h_sign = f"+{h}" if h >= 0 else str(h)
    k_sign = f"+{k}" if k >= 0 else str(k)
    question = (
        f"Il punto P({a}, {b}) viene traslato di vettore ({h}, {k}). "
        f"Qual e' la coordinata {ask} del punto immagine P'?"
    )
    explanation = (
        f"Traslazione di vettore ({h}, {k}): P'(x+h, y+k) = P'({a}{h_sign}, {b}{k_sign}) "
        f"= P'({img_x}, {img_y}). La coordinata {ask} e' {correct_value:.0f}."
    )
    tip = "La traslazione somma il vettore (h, k) alle coordinate del punto: P'(x+h, y+k)."
    return question, correct_value, svg, explanation, tip


def _t1_point_symmetry():
    """Reflect a point through the origin and ask for one coordinate."""
    a = random.choice([v for v in range(-8, 9) if v != 0])
    b = random.choice([v for v in range(-8, 9) if v != 0])
    img_x, img_y = -a, -b
    ask = random.choice(["x", "y"])
    correct_value = float(img_x) if ask == "x" else float(img_y)

    scale = 15
    svg, ox, oy, sc = _svg_coordinate_plane(300, 300, scale)
    svg += _svg_point(ox, oy, sc, a, b, f"P({a},{b})", color="#2a9d8f")
    svg += _svg_point(ox, oy, sc, img_x, img_y, f"P'({img_x},{img_y})", color="#e63946")
    # dashed line through origin
    px1, py1 = ox + a * sc, oy - b * sc
    px2, py2 = ox + img_x * sc, oy - img_y * sc
    svg += _svg_dashed_line(px1, py1, px2, py2, color="#e63946")
    # highlight origin
    svg += f'<circle cx="{ox}" cy="{oy}" r="4" fill="#333"/>'
    svg += _svg_text(ox + 10, oy + 15, "O", color="#333", bold=True, size=12)
    svg += _svg_end()

    question = (
        f"Il punto P({a}, {b}) viene riflesso rispetto all'origine O. "
        f"Qual e' la coordinata {ask} del punto immagine P'?"
    )
    explanation = (
        f"Simmetria rispetto all'origine: (x, y) -> (-x, -y). "
        f"Quindi P'({img_x}, {img_y}). La coordinata {ask} e' {correct_value:.0f}."
    )
    tip = "La simmetria centrale rispetto all'origine cambia segno a entrambe le coordinate: P'(-x, -y)."
    return question, correct_value, svg, explanation, tip


# ============ LEVEL 2 — Transformations ============

def _t2_rotation_90():
    """Rotate a point 90 or 270 degrees CCW around the origin."""
    a = random.choice([v for v in range(-7, 8) if v != 0])
    b = random.choice([v for v in range(-7, 8) if v != 0])
    angle = random.choice([90, 270])

    if angle == 90:
        img_x, img_y = -b, a
        rotation_desc = "90° in senso antiorario"
    else:
        img_x, img_y = b, -a
        rotation_desc = "270° in senso antiorario (equivalente a 90° orario)"

    ask = random.choice(["x", "y"])
    correct_value = float(img_x) if ask == "x" else float(img_y)

    scale = 15
    svg, ox, oy, sc = _svg_coordinate_plane(300, 300, scale)
    svg += _svg_point(ox, oy, sc, a, b, f"P({a},{b})", color="#2a9d8f")
    svg += _svg_point(ox, oy, sc, img_x, img_y, f"P'({img_x},{img_y})", color="#e63946")
    # draw rotation arc from P to P'
    px1, py1 = ox + a * sc, oy - b * sc
    px2, py2 = ox + img_x * sc, oy - img_y * sc
    radius_svg = math.sqrt((a * sc) ** 2 + (b * sc) ** 2)
    # Draw dashed arc
    sweep = 0 if angle == 90 else 1
    large_arc = 0 if angle <= 180 else 1
    svg += (
        f'<path d="M {px1:.1f} {py1:.1f} A {radius_svg:.1f} {radius_svg:.1f} 0 {large_arc} {sweep} {px2:.1f} {py2:.1f}" '
        f'fill="none" stroke="#e76f51" stroke-width="1.5" stroke-dasharray="4,3"/>'
    )
    svg += f'<circle cx="{ox}" cy="{oy}" r="3" fill="#333"/>'
    svg += _svg_text(ox + 10, oy + 15, "O", color="#333", bold=True, size=12)
    svg += _svg_end()

    question = (
        f"Il punto P({a}, {b}) viene ruotato di {rotation_desc} attorno all'origine. "
        f"Qual e' la coordinata {ask} del punto immagine P'?"
    )
    explanation = (
        f"Rotazione di {rotation_desc}: "
    )
    if angle == 90:
        explanation += (
            f"(x, y) -> (-y, x). Quindi P'({-b}, {a}). "
            f"La coordinata {ask} e' {correct_value:.0f}."
        )
    else:
        explanation += (
            f"(x, y) -> (y, -x). Quindi P'({b}, {-a}). "
            f"La coordinata {ask} e' {correct_value:.0f}."
        )
    tip = "Rotazione 90° antioraria: (x,y)->(-y,x). Rotazione 90° oraria (=270° antioraria): (x,y)->(y,-x)."
    return question, correct_value, svg, explanation, tip


def _t2_similarity_lengths():
    """Find the corresponding side of a smaller similar triangle."""
    k = random.choice([1.5, 2, 2.5, 3])
    big_side = random.choice([6, 8, 9, 10, 12, 15, 18, 20])
    small_side = big_side / k
    # Ensure clean number
    while abs(small_side - round(small_side, 1)) > 0.01 and small_side != int(small_side):
        big_side = random.choice([6, 8, 9, 10, 12, 15, 18, 20])
        small_side = big_side / k

    correct_value = small_side

    svg = _svg_start(350, 260)
    # Large triangle
    svg += _svg_polygon([(30, 220), (180, 220), (105, 80)], fill="#f0f7ff")
    svg += _svg_label_known(105, 238, f"{big_side}")
    svg += _svg_text(105, 60, "Grande", color="#555", size=11)
    # Small triangle
    small_base = int(80 / k)
    svg += _svg_polygon([(220, 220), (220 + small_base, 220), (220 + small_base // 2, 220 - int(70 / k))], fill="#fff3e0")
    svg += _svg_label_unknown(220 + small_base // 2, 238, "?")
    svg += _svg_text(220 + small_base // 2, 220 - int(70 / k) - 12, "Piccolo", color="#555", size=11)
    svg += _svg_text(175, 30, f"k = {_fmt(k)}", color="#e63946", bold=True, size=13)
    svg += _svg_end()

    question = (
        f"Due triangoli sono simili con rapporto di similitudine k = {_fmt(k)}. "
        f"Se un lato del triangolo piu' grande misura {_fmt(big_side)}, "
        f"quanto misura il lato corrispondente del triangolo piu' piccolo?"
    )
    explanation = (
        f"Rapporto di similitudine k = {_fmt(k)} significa che il lato grande = k * lato piccolo. "
        f"Quindi lato piccolo = {_fmt(big_side)} / {_fmt(k)} = {_fmt(small_side)}."
    )
    tip = "Nei triangoli simili con rapporto k, i lati corrispondenti stanno nel rapporto k:1."
    return question, correct_value, svg, explanation, tip


def _t2_rotation_180_sum():
    """Rotate a point 180 degrees and ask for the sum of coordinates."""
    a = random.choice([v for v in range(-7, 8) if v != 0])
    b = random.choice([v for v in range(-7, 8) if v != 0])
    # Avoid trivial case where a+b == 0 already
    while a + b == 0:
        b = random.choice([v for v in range(-7, 8) if v != 0])
    img_x, img_y = -a, -b
    correct_value = float(img_x + img_y)

    scale = 15
    svg, ox, oy, sc = _svg_coordinate_plane(300, 300, scale)
    svg += _svg_point(ox, oy, sc, a, b, f"P({a},{b})", color="#2a9d8f")
    svg += _svg_point(ox, oy, sc, img_x, img_y, f"P'({img_x},{img_y})", color="#e63946")
    svg += _svg_dashed_line(ox + a * sc, oy - b * sc, ox + img_x * sc, oy - img_y * sc, color="#e63946")
    svg += f'<circle cx="{ox}" cy="{oy}" r="3" fill="#333"/>'
    svg += _svg_text(ox + 10, oy + 15, "O", color="#333", bold=True, size=12)
    svg += _svg_end()

    question = (
        f"Dopo una rotazione di 180° attorno all'origine, il punto P({a}, {b}) "
        f"ha coordinate P'(x, y). Quanto vale x + y?"
    )
    explanation = (
        f"Rotazione di 180°: (x, y) -> (-x, -y). "
        f"Quindi P'({img_x}, {img_y}). "
        f"x + y = {img_x} + ({img_y}) = {img_x + img_y}."
    )
    tip = "La rotazione di 180° attorno all'origine equivale alla simmetria centrale: (x,y)->(-x,-y)."
    return question, correct_value, svg, explanation, tip


# ============ LEVEL 3 — Transformations ============

def _t3_similarity_area():
    """Area scaling with similarity ratio k: area scales by k^2."""
    k = random.choice([2, 3, 1.5, 2.5])
    use_volume = random.choice([True, False])

    if use_volume:
        small_vol = random.choice([4, 8, 10, 12, 16, 20, 27])
        correct_value = small_vol * k ** 3
        quantity = "volume"
        formula = "k^3"
        power = 3
    else:
        small_area = random.choice([4, 6, 8, 9, 10, 12, 16, 25])
        correct_value = small_area * k ** 2
        quantity = "area"
        formula = "k^2"
        power = 2

    measure = small_vol if use_volume else small_area

    svg = _svg_start(350, 220)
    if use_volume:
        # Two cubes (simplified)
        svg += _svg_polygon([(30, 170), (90, 170), (90, 110), (30, 110)], fill="#f0f7ff")
        svg += _svg_polygon([(40, 100), (100, 100), (100, 160), (40, 160)], fill="#dbe9f7")
        svg += _svg_text(60, 190, f"V = {measure}", color="#2a9d8f", bold=True, size=11)
        big_size = int(60 * min(k, 2.5))
        svg += _svg_polygon([(160, 170), (160 + big_size, 170), (160 + big_size, 170 - big_size), (160, 170 - big_size)], fill="#fff3e0")
        svg += _svg_text(160 + big_size // 2, 190, "V = ?", color="#e63946", bold=True, size=11)
    else:
        svg += _svg_polygon([(30, 180), (100, 180), (65, 120)], fill="#f0f7ff")
        svg += _svg_text(65, 198, f"A = {measure}", color="#2a9d8f", bold=True, size=11)
        big_base = int(70 * min(k, 2.5))
        svg += _svg_polygon([(160, 180), (160 + big_base, 180), (160 + big_base // 2, 180 - int(60 * min(k, 2.5)))], fill="#fff3e0")
        svg += _svg_text(160 + big_base // 2, 198, "A = ?", color="#e63946", bold=True, size=11)
    svg += _svg_text(175, 20, f"k = {_fmt(k)}", color="#e63946", bold=True, size=13)
    svg += _svg_end()

    question = (
        f"Due figure sono simili con rapporto di similitudine k = {_fmt(k)}. "
        f"Se il {quantity} della figura piccola e' {measure}, "
        f"qual e' il {quantity} della figura grande?"
    )
    explanation = (
        f"Per figure simili con rapporto k, il {quantity} scala con {formula}. "
        f"{quantity.capitalize()} grande = {measure} * {_fmt(k)}^{power} = {measure} * {_fmt(k ** power)} = {_fmt(correct_value)}."
    )
    tip = f"Per figure simili: le lunghezze scalano con k, le aree con k^2, i volumi con k^3."
    return question, correct_value, svg, explanation, tip


def _t3_compose_transformations():
    """Apply two transformations in sequence: translation then reflection."""
    a = random.choice([v for v in range(-5, 6) if v != 0])
    b = random.choice([v for v in range(-5, 6) if v != 0])
    h = random.choice([v for v in range(-4, 5) if v != 0])
    k = random.choice([v for v in range(-4, 5) if v != 0])

    # Step 1: translate
    mid_x = a + h
    mid_y = b + k
    # Step 2: reflect across x-axis
    final_x = mid_x
    final_y = -mid_y
    correct_value = float(final_y)

    scale = 12
    svg, ox, oy, sc = _svg_coordinate_plane(300, 300, scale)
    svg += _svg_point(ox, oy, sc, a, b, f"P({a},{b})", color="#2a9d8f")
    svg += _svg_point(ox, oy, sc, mid_x, mid_y, f"P\u2081({mid_x},{mid_y})", color="#e76f51")
    svg += _svg_point(ox, oy, sc, final_x, final_y, f"P'({final_x},{final_y})", color="#e63946")
    # arrows
    px0, py0 = ox + a * sc, oy - b * sc
    px1, py1 = ox + mid_x * sc, oy - mid_y * sc
    px2, py2 = ox + final_x * sc, oy - final_y * sc
    svg += _svg_arrow(px0, py0, px1, py1, color="#e76f51")
    svg += _svg_dashed_line(px1, py1, px2, py2, color="#e63946")
    # highlight x-axis
    svg += _svg_line(10, oy, 290, oy, color="#e76f51", width=2)
    svg += _svg_end()

    h_sign = f"+{h}" if h >= 0 else str(h)
    k_sign = f"+{k}" if k >= 0 else str(k)
    question = (
        f"Il punto P({a}, {b}) viene prima traslato di vettore ({h}, {k}), "
        f"poi riflesso rispetto all'asse x. "
        f"Qual e' la coordinata y del punto finale P'?"
    )
    explanation = (
        f"Passo 1 - Traslazione: P({a},{b}) + ({h},{k}) = P\u2081({mid_x}, {mid_y}).\n"
        f"Passo 2 - Riflessione asse x: (x, y) -> (x, -y). "
        f"P'({final_x}, {final_y}). La coordinata y e' {final_y}."
    )
    tip = "Nelle trasformazioni composte, applica le operazioni nell'ordine indicato. L'ordine conta!"
    return question, correct_value, svg, explanation, tip


def _t3_transformation_vertices():
    """Translate a triangle and ask for the sum of x-coordinates of new vertices."""
    for _attempt in range(200):
        x1 = random.randint(-4, 4)
        y1 = random.randint(-4, 4)
        x2 = random.randint(-4, 4)
        y2 = random.randint(-4, 4)
        x3 = random.randint(-4, 4)
        y3 = random.randint(-4, 4)
        area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
        if area >= 1:
            break
    else:
        # Fallback: guaranteed non-degenerate
        x1, y1, x2, y2, x3, y3 = 0, 0, 3, 0, 0, 4

    h = random.choice([v for v in range(-5, 6) if v != 0])
    k = random.choice([v for v in range(-5, 6) if v != 0])

    sum_new_x = (x1 + h) + (x2 + h) + (x3 + h)
    correct_value = float(sum_new_x)

    scale = 14
    svg, ox, oy, sc = _svg_coordinate_plane(340, 300, scale, origin=(170, 150))
    # Original triangle
    pts_orig = [
        (ox + x1 * sc, oy - y1 * sc),
        (ox + x2 * sc, oy - y2 * sc),
        (ox + x3 * sc, oy - y3 * sc),
    ]
    svg += _svg_polygon(pts_orig, fill="#f0f7ff", stroke="#2a9d8f")
    svg += _svg_text(pts_orig[0][0], pts_orig[0][1] - 8, f"A({x1},{y1})", color="#2a9d8f", size=10)
    svg += _svg_text(pts_orig[1][0], pts_orig[1][1] - 8, f"B({x2},{y2})", color="#2a9d8f", size=10)
    svg += _svg_text(pts_orig[2][0], pts_orig[2][1] - 8, f"C({x3},{y3})", color="#2a9d8f", size=10)
    # Translated triangle
    pts_new = [
        (ox + (x1 + h) * sc, oy - (y1 + k) * sc),
        (ox + (x2 + h) * sc, oy - (y2 + k) * sc),
        (ox + (x3 + h) * sc, oy - (y3 + k) * sc),
    ]
    svg += _svg_polygon(pts_new, fill="#fff3e0", stroke="#e63946")
    svg += _svg_text(170, 290, f"vettore ({h}, {k})", color="#555", size=12)
    svg += _svg_end()

    question = (
        f"Il triangolo con vertici A({x1},{y1}), B({x2},{y2}), C({x3},{y3}) "
        f"viene traslato di vettore ({h}, {k}). "
        f"Qual e' la somma delle coordinate x dei nuovi vertici?"
    )
    explanation = (
        f"I nuovi vertici sono: A'({x1 + h},{y1 + k}), B'({x2 + h},{y2 + k}), C'({x3 + h},{y3 + k}).\n"
        f"Somma delle x: ({x1 + h}) + ({x2 + h}) + ({x3 + h}) = "
        f"{x1} + {x2} + {x3} + 3*{h} = {x1 + x2 + x3} + {3 * h} = {sum_new_x}."
    )
    tip = "Quando si trasla un poligono, ogni vertice si sposta dello stesso vettore. La somma delle x cresce di n*h (n = numero vertici)."
    return question, correct_value, svg, explanation, tip


# ============ SIMILAR TRIANGLES — EXPANDED ============

def _t2_similar_find_side():
    """Find unknown side of a similar triangle via proportion (3 known sides + 1)."""
    # Triangle A sides
    a1 = random.randint(3, 8)
    a2 = random.randint(3, 8)
    a3 = random.randint(3, 8)
    # Scale factor (clean values)
    k = random.choice([1.5, 2, 2.5, 3, 4])
    # Triangle B: one known side, find corresponding side
    which = random.randint(0, 2)  # which side of A maps to the known side of B
    sides_a = [a1, a2, a3]
    sides_b_known_idx = which
    b_known = sides_a[sides_b_known_idx] * k
    # Ask for a different corresponding side
    ask_idx = (which + 1) % 3
    correct_value = sides_a[ask_idx] * k

    # SVG: two triangles side by side
    svg = _svg_start(380, 260)
    # Small triangle (A)
    svg += _svg_polygon([(30, 220), (130, 220), (80, 100)], fill="#f0f7ff")
    svg += _svg_text(80, 80, "A", color="#555", size=13)
    labels_a = [
        ((30 + 130) // 2, 238),   # bottom side
        ((130 + 80) // 2 + 15, (220 + 100) // 2),  # right side
        ((30 + 80) // 2 - 15, (220 + 100) // 2),   # left side
    ]
    for i, (lx, ly) in enumerate(labels_a):
        svg += _svg_label_known(lx, ly, f"{sides_a[i]}")

    # Large triangle (B)
    svg += _svg_polygon([(200, 220), (340, 220), (270, 80)], fill="#fff3e0")
    svg += _svg_text(270, 60, "B", color="#555", size=13)
    labels_b = [
        ((200 + 340) // 2, 238),
        ((340 + 270) // 2 + 15, (220 + 80) // 2),
        ((200 + 270) // 2 - 15, (220 + 80) // 2),
    ]
    for i, (lx, ly) in enumerate(labels_b):
        if i == sides_b_known_idx:
            svg += _svg_label_known(lx, ly, f"{_fmt(b_known)}")
        elif i == ask_idx:
            svg += _svg_label_unknown(lx, ly, "?")
        else:
            svg += _svg_text(lx, ly, "—", color="#aaa", size=11)

    svg += _svg_text(190, 30, "Triangoli simili", color="#555", size=14)
    svg += _svg_end()

    side_names = ["primo", "secondo", "terzo"]
    question = (
        f"Due triangoli sono simili. Il triangolo A ha lati {a1}, {a2} e {a3}. "
        f"Nel triangolo B il lato corrispondente al {side_names[sides_b_known_idx]} lato di A "
        f"misura {_fmt(b_known)}. Quanto misura il lato di B corrispondente "
        f"al {side_names[ask_idx]} lato di A?"
    )
    explanation = (
        f"Rapporto di similitudine k = {_fmt(b_known)} / {sides_a[sides_b_known_idx]} = {_fmt(k)}. "
        f"Lato cercato = {sides_a[ask_idx]} * {_fmt(k)} = {_fmt(correct_value)}."
    )
    tip = "Per trovare un lato incognito di un triangolo simile, prima calcola il rapporto k, poi moltiplica."
    return question, correct_value, svg, explanation, tip


def _t2_similar_scale_factor():
    """Determine the scale factor between two similar triangles."""
    k = random.choice([1.5, 2, 2.5, 3, 4, 5])
    base_side = random.randint(3, 10)
    big_side = base_side * k

    svg = _svg_start(380, 260)
    # Small triangle
    s = min(80, base_side * 10)
    svg += _svg_polygon([(30, 220), (30 + s, 220), (30 + s // 2, 220 - int(s * 0.8))], fill="#f0f7ff")
    svg += _svg_label_known(30 + s // 2, 238, f"{base_side}")
    svg += _svg_text(30 + s // 2, 220 - int(s * 0.8) - 12, "Piccolo", color="#555", size=11)

    # Large triangle
    b = min(160, int(big_side * 10))
    lx = 200
    svg += _svg_polygon([(lx, 220), (lx + b, 220), (lx + b // 2, 220 - int(b * 0.8))], fill="#fff3e0")
    svg += _svg_label_known(lx + b // 2, 238, f"{_fmt(big_side)}")
    svg += _svg_text(lx + b // 2, 220 - int(b * 0.8) - 12, "Grande", color="#555", size=11)

    svg += _svg_text(190, 25, "k = ?", color="#e63946", bold=True, size=14)
    svg += _svg_end()

    question = (
        f"Due triangoli sono simili. Un lato del triangolo piccolo misura {base_side} "
        f"e il lato corrispondente del triangolo grande misura {_fmt(big_side)}. "
        f"Qual e' il rapporto di similitudine k (grande/piccolo)?"
    )
    explanation = (
        f"k = lato grande / lato piccolo = {_fmt(big_side)} / {base_side} = {_fmt(k)}."
    )
    tip = "Il rapporto di similitudine k e' il rapporto tra i lati corrispondenti: k = lato grande / lato piccolo."
    return question, k, svg, explanation, tip


def _t2_similar_area_ratio():
    """Given scale factor k, find area of larger figure from area of smaller."""
    k = random.choice([2, 3, 1.5, 2.5, 4])
    small_area = random.choice([4, 6, 8, 9, 10, 12, 16, 20, 25])
    correct_value = small_area * k * k

    svg = _svg_start(380, 220)
    # Small triangle
    svg += _svg_polygon([(30, 180), (100, 180), (65, 120)], fill="#f0f7ff")
    svg += _svg_text(65, 198, f"A = {small_area}", color="#2a9d8f", bold=True, size=11)
    svg += _svg_text(65, 108, "Piccolo", color="#555", size=11)
    # Large triangle
    big_base = min(int(70 * min(k, 3)), 160)
    big_h = min(int(60 * min(k, 3)), 140)
    svg += _svg_polygon([(160, 180), (160 + big_base, 180), (160 + big_base // 2, 180 - big_h)], fill="#fff3e0")
    svg += _svg_text(160 + big_base // 2, 198, "A = ?", color="#e63946", bold=True, size=11)
    svg += _svg_text(160 + big_base // 2, 180 - big_h - 12, "Grande", color="#555", size=11)
    svg += _svg_text(190, 20, f"k = {_fmt(k)}", color="#e63946", bold=True, size=14)
    svg += _svg_end()

    question = (
        f"Due figure sono simili con rapporto di similitudine k = {_fmt(k)}. "
        f"L'area della figura piccola e' {small_area} cm^2. "
        f"Qual e' l'area della figura grande?"
    )
    explanation = (
        f"Per figure simili, l'area scala con k^2. "
        f"Area grande = {small_area} * {_fmt(k)}^2 = {small_area} * {_fmt(k * k)} = {_fmt(correct_value)} cm^2."
    )
    tip = "Nei triangoli simili con rapporto k, le aree stanno nel rapporto k^2."
    return question, correct_value, svg, explanation, tip


def _t3_similar_real_world():
    """Real-world similarity: shadow/height proportion to find tree height."""
    person_h = random.choice([1.6, 1.7, 1.75, 1.8, 1.85])
    person_shadow = random.choice([2.0, 2.5, 3.0, 3.5, 4.0])
    tree_shadow = random.choice([8, 10, 12, 14, 15, 16, 18, 20])
    # tree_h / tree_shadow = person_h / person_shadow
    correct_value = person_h * tree_shadow / person_shadow

    svg = _svg_start(380, 260)
    # Ground line
    svg += _svg_line(10, 220, 370, 220, color="#aaa", width=1)
    # Person (stick figure)
    px = 60
    p_scale = 30
    svg += _svg_line(px, 220, px, 220 - int(person_h * p_scale), color="#2a9d8f", width=3)
    svg += _svg_circle(px, 220 - int(person_h * p_scale) - 5, 5, fill="#2a9d8f", stroke="#2a9d8f", width=1)
    svg += _svg_label_known(px - 25, 220 - int(person_h * p_scale * 0.5), f"{person_h} m")
    # Person shadow
    svg += _svg_line(px, 220, px + int(person_shadow * 15), 220, color="#f4a261", width=3)
    svg += _svg_label_known(px + int(person_shadow * 7.5), 235, f"{_fmt(person_shadow)} m")
    # Tree
    tx = 220
    t_scale = 8
    tree_h_display = min(int(correct_value * t_scale), 160)
    svg += _svg_line(tx, 220, tx, 220 - tree_h_display, color="#2a9d8f", width=5)
    # Tree crown
    svg += _svg_polygon(
        [(tx - 20, 220 - tree_h_display + 10), (tx + 20, 220 - tree_h_display + 10), (tx, 220 - tree_h_display - 15)],
        fill="#a7c957", stroke="#6a994e", width=2
    )
    svg += _svg_label_unknown(tx - 30, 220 - tree_h_display // 2, "? m")
    # Tree shadow
    svg += _svg_line(tx, 220, tx + int(tree_shadow * 5), 220, color="#f4a261", width=3)
    svg += _svg_label_known(tx + int(tree_shadow * 2.5), 235, f"{tree_shadow} m")
    svg += _svg_text(190, 20, "Ombre proporzionali", color="#555", size=13)
    svg += _svg_end()

    question = (
        f"Una persona alta {_fmt(person_h)} m proietta un'ombra di {_fmt(person_shadow)} m. "
        f"Nello stesso momento, un albero proietta un'ombra di {tree_shadow} m. "
        f"Qual e' l'altezza dell'albero?"
    )
    explanation = (
        f"Per similitudine dei triangoli formati dai raggi del sole: "
        f"altezza_albero / ombra_albero = altezza_persona / ombra_persona. "
        f"altezza_albero = {_fmt(person_h)} * {tree_shadow} / {_fmt(person_shadow)} = {_fmt(correct_value)} m."
    )
    tip = "Quando il sole colpisce con lo stesso angolo, i triangoli ombra-oggetto sono simili."
    return question, correct_value, svg, explanation, tip


# ============ TRIGONOMETRIC RATIOS — EXPANDED ============

def _t2_trig_find_ratio():
    """Given a right triangle with labeled sides, find sin/cos/tan of a specified angle."""
    a = random.randint(3, 12)
    b = random.randint(3, 12)
    c = math.sqrt(a * a + b * b)
    # Choose which trig function to ask about
    func_name = random.choice(["sin", "cos", "tan"])
    # angle alpha at vertex between hypotenuse and adjacent side 'a'
    # opp = b, adj = a, hyp = c
    if func_name == "sin":
        correct_value = b / c
        formula_str = f"cateto opposto / ipotenusa = {b} / {_fmt(c)}"
    elif func_name == "cos":
        correct_value = a / c
        formula_str = f"cateto adiacente / ipotenusa = {a} / {_fmt(c)}"
    else:
        correct_value = b / a
        formula_str = f"cateto opposto / cateto adiacente = {b} / {a}"

    # SVG: right triangle with labeled sides
    ox, oy = 50, 210
    bx, by = ox + a * 12, oy
    tx, ty = ox, oy - b * 12
    svg = _svg_start()
    svg += _svg_polygon([(ox, oy), (bx, by), (tx, ty)], fill="#f0f7ff")
    svg += _svg_right_angle(ox, oy, 0, 90)
    svg += _svg_label_known((ox + bx) / 2, oy + 20, f"{a}")
    svg += _svg_label_known(ox - 20, (oy + ty) / 2, f"{b}")
    svg += _svg_label_known((bx + tx) / 2 + 15, (by + ty) / 2, _fmt(c))
    # Mark the angle alpha at vertex B (bottom-right)
    alpha_deg = math.degrees(math.atan2(b, a))
    svg += _svg_arc_angle(bx, by, 90 + alpha_deg, 180, radius=20, label="α")
    svg += _svg_end()

    question = (
        f"Un triangolo rettangolo ha cateti {a} e {b} e ipotenusa {_fmt(c)}. "
        f"Quanto vale {func_name}(α), dove α e' l'angolo in basso a destra?"
    )
    explanation = (
        f"{func_name}(α) = {formula_str} = {_fmt(correct_value)}."
    )
    tip = "SOH-CAH-TOA: sin = opposto/ipotenusa, cos = adiacente/ipotenusa, tan = opposto/adiacente."
    return question, correct_value, svg, explanation, tip


def _t2_trig_find_side():
    """Given an angle and one side of a right triangle, find another side using trig."""
    angle_deg = random.choice([30, 45, 60])
    angle_rad = math.radians(angle_deg)
    # Choose what is given and what to find
    scenario = random.choice(["hyp_find_opp", "hyp_find_adj", "adj_find_opp"])

    if scenario == "hyp_find_opp":
        hyp = random.randint(5, 20)
        correct_value = hyp * math.sin(angle_rad)
        opp = correct_value
        adj = hyp * math.cos(angle_rad)
        given_str = f"ipotenusa = {hyp}"
        ask_str = "il cateto opposto all'angolo"
        formula = f"{hyp} * sin({angle_deg}°) = {hyp} * {_fmt(math.sin(angle_rad))} = {_fmt(correct_value)}"
    elif scenario == "hyp_find_adj":
        hyp = random.randint(5, 20)
        correct_value = hyp * math.cos(angle_rad)
        adj = correct_value
        opp = hyp * math.sin(angle_rad)
        given_str = f"ipotenusa = {hyp}"
        ask_str = "il cateto adiacente all'angolo"
        formula = f"{hyp} * cos({angle_deg}°) = {hyp} * {_fmt(math.cos(angle_rad))} = {_fmt(correct_value)}"
    else:
        adj = random.randint(5, 15)
        correct_value = adj * math.tan(angle_rad)
        opp = correct_value
        hyp = math.sqrt(adj * adj + opp * opp)
        given_str = f"cateto adiacente = {adj}"
        ask_str = "il cateto opposto all'angolo"
        formula = f"{adj} * tan({angle_deg}°) = {adj} * {_fmt(math.tan(angle_rad))} = {_fmt(correct_value)}"

    # SVG
    ox, oy = 50, 210
    scale = min(12, 180 / max(adj, opp, 1))
    bx, by = ox + int(adj * scale), oy
    tx, ty = ox, oy - int(opp * scale)
    svg = _svg_start()
    svg += _svg_polygon([(ox, oy), (bx, by), (tx, ty)], fill="#f0f7ff")
    svg += _svg_right_angle(ox, oy, 0, 90)
    svg += _svg_arc_angle(bx, by, 90 + angle_deg, 180, radius=22, label=f"{angle_deg}°")

    if scenario == "hyp_find_opp":
        svg += _svg_label_known((bx + tx) / 2 + 15, (by + ty) / 2, f"{hyp}")
        svg += _svg_label_unknown(ox - 18, (oy + ty) / 2, "?")
    elif scenario == "hyp_find_adj":
        svg += _svg_label_known((bx + tx) / 2 + 15, (by + ty) / 2, f"{hyp}")
        svg += _svg_label_unknown((ox + bx) / 2, oy + 20, "?")
    else:
        svg += _svg_label_known((ox + bx) / 2, oy + 20, f"{adj}")
        svg += _svg_label_unknown(ox - 18, (oy + ty) / 2, "?")
    svg += _svg_end()

    question = (
        f"Un triangolo rettangolo ha {given_str} e un angolo acuto di {angle_deg}°. "
        f"Quanto misura {ask_str}?"
    )
    explanation = f"Cateto cercato = {formula}."
    tip = "SOH-CAH-TOA: sin = opposto/ipotenusa, cos = adiacente/ipotenusa, tan = opposto/adiacente."
    return question, correct_value, svg, explanation, tip


def _t3_trig_identify_angle():
    """Given two sides of a right triangle, find an angle in degrees."""
    angle_deg = random.choice([30, 45, 60])
    angle_rad = math.radians(angle_deg)
    hyp = random.randint(5, 15)
    opp = hyp * math.sin(angle_rad)
    adj = hyp * math.cos(angle_rad)

    # Choose which ratio to present
    ratio_type = random.choice(["sin", "cos", "tan"])
    if ratio_type == "sin":
        ratio_str = f"{_fmt(opp)} / {_fmt(hyp)}"
        ratio_desc = "cateto opposto / ipotenusa"
        func_inv = "arcsin"
    elif ratio_type == "cos":
        ratio_str = f"{_fmt(adj)} / {_fmt(hyp)}"
        ratio_desc = "cateto adiacente / ipotenusa"
        func_inv = "arccos"
    else:
        ratio_str = f"{_fmt(opp)} / {_fmt(adj)}"
        ratio_desc = "cateto opposto / cateto adiacente"
        func_inv = "arctan"

    correct_value = float(angle_deg)

    # SVG
    ox, oy = 50, 210
    scale = min(12, 180 / max(adj, opp, 1))
    bx, by = ox + int(adj * scale), oy
    tx, ty = ox, oy - int(opp * scale)
    svg = _svg_start()
    svg += _svg_polygon([(ox, oy), (bx, by), (tx, ty)], fill="#f0f7ff")
    svg += _svg_right_angle(ox, oy, 0, 90)
    svg += _svg_label_known((ox + bx) / 2, oy + 20, _fmt(adj))
    svg += _svg_label_known(ox - 18, (oy + ty) / 2, _fmt(opp))
    svg += _svg_label_known((bx + tx) / 2 + 15, (by + ty) / 2, f"{hyp}")
    svg += _svg_arc_angle(bx, by, 90 + angle_deg, 180, radius=22, label="α = ?")
    svg += _svg_end()

    question = (
        f"Un triangolo rettangolo ha cateto opposto {_fmt(opp)}, "
        f"cateto adiacente {_fmt(adj)} e ipotenusa {hyp}. "
        f"Quanto vale l'angolo α (in gradi) sapendo che "
        f"{ratio_type}(α) = {ratio_desc} = {ratio_str}?"
    )
    explanation = (
        f"α = {func_inv}({ratio_str}) = {angle_deg}°."
    )
    tip = "Gli angoli notevoli da ricordare: sin(30°)=0.5, sin(45°)=√2/2≈0.71, sin(60°)=√3/2≈0.87."
    return question, correct_value, svg, explanation, tip


def _t3_trig_real_world():
    """Real-world trig: find height of building from distance and elevation angle."""
    angle_deg = random.choice([30, 45, 60])
    angle_rad = math.radians(angle_deg)
    distance = random.choice([10, 15, 20, 25, 30, 40, 50])
    # height = distance * tan(angle)
    correct_value = distance * math.tan(angle_rad)

    # SVG: building + observer
    svg = _svg_start(380, 260)
    # Ground
    svg += _svg_line(10, 230, 370, 230, color="#aaa", width=1)
    # Observer
    obs_x = 60
    svg += _svg_line(obs_x, 230, obs_x, 200, color="#2a9d8f", width=3)
    svg += _svg_circle(obs_x, 195, 5, fill="#2a9d8f", stroke="#2a9d8f", width=1)
    # Building
    bld_x = 300
    bld_h = min(int(correct_value * 3), 170)
    svg += _svg_polygon(
        [(bld_x - 25, 230), (bld_x + 25, 230), (bld_x + 25, 230 - bld_h), (bld_x - 25, 230 - bld_h)],
        fill="#dbe9f7", stroke="#333", width=2
    )
    svg += _svg_label_unknown(bld_x + 40, 230 - bld_h // 2, "h = ?")
    # Distance label
    svg += _svg_label_known((obs_x + bld_x) / 2, 245, f"{distance} m")
    # Angle of elevation line (dashed)
    svg += f'<line x1="{obs_x}" y1="200" x2="{bld_x}" y2="{230 - bld_h}" stroke="#e63946" stroke-width="1.5" stroke-dasharray="4,4"/>'
    # Angle arc
    svg += _svg_arc_angle(obs_x, 200, -angle_deg, 0, radius=30, label=f"{angle_deg}°")
    svg += _svg_end()

    question = (
        f"Un osservatore si trova a {distance} m dalla base di un edificio. "
        f"L'angolo di elevazione dalla sua posizione alla cima dell'edificio e' di {angle_deg}°. "
        f"Qual e' l'altezza dell'edificio? (ignora l'altezza dell'osservatore)"
    )
    explanation = (
        f"tan({angle_deg}°) = altezza / distanza. "
        f"Altezza = {distance} * tan({angle_deg}°) = {distance} * {_fmt(math.tan(angle_rad))} "
        f"= {_fmt(correct_value)} m."
    )
    tip = "Per problemi di angolo di elevazione: altezza = distanza * tan(angolo)."
    return question, correct_value, svg, explanation, tip


class GeometrySherlock(Exercise):
    """Sherlock Geometrico -- geometric figures with partial data and progressive clues."""

    TEMPLATES_L1 = [
        _t1_pythagoras_hypotenuse,
        _t1_pythagoras_leg,
        _t1_rectangle_area,
        _t1_circle_area,
        _t1_triangle_area,
        _t1_cylinder_volume,
        _t1_rectangular_prism_volume,
        _t1_axial_symmetry,
        _t1_translation,
        _t1_point_symmetry,
    ]

    TEMPLATES_L2 = [
        _t2_pythagoras_plus_area,
        _t2_similar_triangles,
        _t2_trapezoid_area,
        _t2_circle_sector_area,
        _t2_trig_right_triangle,
        _t2_perimeter_composite,
        _t2_inscribed_angle,
        _t2_chord_distance,
        _t2_cone_volume,
        _t2_sphere_volume,
        _t2_pyramid_volume,
        _t2_rotation_90,
        _t2_similarity_lengths,
        _t2_rotation_180_sum,
        _t2_similar_find_side,
        _t2_similar_scale_factor,
        _t2_similar_area_ratio,
        _t2_trig_find_ratio,
        _t2_trig_find_side,
    ]

    TEMPLATES_L3 = [
        _t3_distance_two_points,
        _t3_midpoint_and_distance,
        _t3_triangle_area_coordinates,
        _t3_circle_tangent_length,
        _t3_line_intersection_area,
        _t3_inscribed_square_circle,
        _t3_arc_length,
        _t3_power_of_point,
        _t3_composite_cylinder_cone,
        _t3_sphere_inscribed_in_cylinder,
        _t3_similarity_area,
        _t3_compose_transformations,
        _t3_transformation_vertices,
        _t3_similar_real_world,
        _t3_trig_identify_angle,
        _t3_trig_real_world,
    ]

    # Templates whose answers can be negative or zero, requiring signed distractors
    _SIGNED_TEMPLATES = {
        _t1_axial_symmetry,
        _t1_translation,
        _t1_point_symmetry,
        _t2_rotation_90,
        _t2_rotation_180_sum,
        _t3_compose_transformations,
        _t3_transformation_vertices,
    }

    def generate(self, difficulty: int, text_only: bool = False) -> dict:
        """Generate a geometry exercise.

        Args:
            difficulty: 1-3 difficulty level.
            text_only: If True, suppress SVG graph_data (for exam simulation
                       realism — real TOLC-B geometry is text-only).
        """
        difficulty = max(1, min(3, difficulty))

        if difficulty == 1:
            templates = self.TEMPLATES_L1
        elif difficulty == 2:
            templates = self.TEMPLATES_L2
        else:
            templates = self.TEMPLATES_L3

        template_fn = random.choice(templates)
        question, correct_value, svg, explanation, tip = template_fn()

        correct_str = _fmt(correct_value)
        if template_fn in self._SIGNED_TEMPLATES:
            distractors = _distractor_signed(correct_value)
        else:
            distractors = _distractor(correct_value)

        options = [correct_str] + distractors
        correct_index = 0
        options, correct_index = Exercise.shuffle_options(options, correct_index)

        return {
            "question": question,
            "graph_data": None if text_only else svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": tip,
            "difficulty": difficulty,
        }
