#!/usr/bin/env python3
import math

# --- KONFIGURATION ---
FILENAME = "loompanics_spiral_strong_001.svg"
SIZE = 1000
CENTER = SIZE / 2
NUM_ARMS = 24           # Anzahl der Arme
STEPS = 200             # Höhere Auflösung für glatte Kurven bei starker Drehung
ROTATIONS = 1.5         # WIE OFT wickelt sich ein Arm um die Mitte? (3 = extrem)
ARM_WIDTH = 0.5         # Breite der Arme (0.5 = 50% gefüllt)
COLOR = "#FFD700"       # Gold

def generate():
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">',
        '  <defs>',
        f'    <radialGradient id="grad" cx="{CENTER}" cy="{CENTER}" r="{CENTER}" gradientUnits="userSpaceOnUse">',
        f'      <stop offset="0%" stop-color="{COLOR}" stop-opacity="1"/>',
        f'      <stop offset="100%" stop-color="{COLOR}" stop-opacity="0"/>',
        '    </radialGradient>',
        '  </defs>',
        # Hintergrund schwarz optional für besseren Kontrast beim Testen (hier auskommentiert)
        # f'<rect width="{SIZE}" height="{SIZE}" fill="black" />',
        '  <g>'
    ]

    angle_step_deg = 360 / NUM_ARMS
    wedge_width_deg = angle_step_deg * ARM_WIDTH
    max_radius = SIZE * 0.9 # Geht fast bis zum Rand

    for i in range(NUM_ARMS):
        start_angle_deg = i * angle_step_deg
        
        points_left = []
        points_right = []

        for s in range(STEPS + 1):
            t = s / STEPS # 0.0 bis 1.0
            r = t * max_radius
            
            # Der Twist: Linearer Anstieg der Rotation basierend auf dem Radius
            # Totaler Twist am Ende = ROTATIONS * 360 Grad
            twist_deg = t * ROTATIONS * 360
            
            # Basis-Winkel für diesen Schritt
            current_angle_deg = start_angle_deg + twist_deg
            
            # Linke und Rechte Kante berechnen
            a_left_rad = math.radians(current_angle_deg - (wedge_width_deg / 2))
            a_right_rad = math.radians(current_angle_deg + (wedge_width_deg / 2))

            # Polar -> Kartesisch
            x1 = CENTER + r * math.cos(a_left_rad)
            y1 = CENTER + r * math.sin(a_left_rad)
            
            x2 = CENTER + r * math.cos(a_right_rad)
            y2 = CENTER + r * math.sin(a_right_rad)

            points_left.append(f"{x1:.2f} {y1:.2f}")
            points_right.append(f"{x2:.2f} {y2:.2f}")

        # Pfad schließen
        d = f"M {CENTER} {CENTER} " 
        d += " L ".join(points_left)
        # Rechte Seite rückwärts, damit der Pfad sauber zurück zum Zentrum läuft
        d += " L " + " L ".join(reversed(points_right))
        d += " Z"

        svg.append(f'    <path d="{d}" fill="url(#grad)" />')

    svg.append('  </g></svg>')

    with open(FILENAME, "w") as f:
        f.write("\n".join(svg))
    
    print(f"[SUCCESS] {FILENAME} mit {ROTATIONS} Umdrehungen generiert.")

if __name__ == "__main__":
    generate()
