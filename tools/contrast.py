"""WCAG 2.x contrast between color pairs. Usage: python3 -I contrast.py '#7A285A' '#FFFFFF' ['#2D2430' '#FFF8F6' ...]
Consecutive pairs (text, background). Prints the ratio and level: AAA >= 7, AA >= 4.5, AA large/UI >= 3."""
import sys


def lum(hexcor):
    h = hexcor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def razao(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main(args):
    if len(args) < 2 or len(args) % 2:
        sys.exit(__doc__)
    for texto, fundo in zip(args[::2], args[1::2]):
        r = razao(texto, fundo)
        nivel = "AAA" if r >= 7 else "AA" if r >= 4.5 else "AA large/UI" if r >= 3 else "FAIL"
        print(f"{texto} on {fundo}: {r:.2f}:1  {nivel}")


if __name__ == "__main__":
    main(sys.argv[1:])
