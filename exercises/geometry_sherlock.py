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
    x1, y1 = random.randint(-3, 3), random.randint(-3, 3)
    x2, y2 = random.randint(-3, 3), random.randint(-3, 3)
    x3, y3 = random.randint(-3, 3), random.randint(-3, 3)
    area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
    while area < 1:
        x3 = random.randint(-3, 3)
        y3 = random.randint(-3, 3)
        area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2

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


class GeometrySherlock(Exercise):
    """Sherlock Geometrico -- geometric figures with partial data and progressive clues."""

    TEMPLATES_L1 = [
        _t1_pythagoras_hypotenuse,
        _t1_pythagoras_leg,
        _t1_rectangle_area,
        _t1_circle_area,
        _t1_triangle_area,
    ]

    TEMPLATES_L2 = [
        _t2_pythagoras_plus_area,
        _t2_similar_triangles,
        _t2_trapezoid_area,
        _t2_circle_sector_area,
        _t2_trig_right_triangle,
        _t2_perimeter_composite,
    ]

    TEMPLATES_L3 = [
        _t3_distance_two_points,
        _t3_midpoint_and_distance,
        _t3_triangle_area_coordinates,
        _t3_circle_tangent_length,
        _t3_line_intersection_area,
        _t3_inscribed_square_circle,
    ]

    def generate(self, difficulty: int) -> dict:
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
        distractors = _distractor(correct_value)

        options = [correct_str] + distractors
        correct_index = 0
        options, correct_index = Exercise.shuffle_options(options, correct_index)

        return {
            "question": question,
            "graph_data": svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": tip,
            "difficulty": difficulty,
        }
