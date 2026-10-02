# Geometry helper tools
from math import pi, sin, cos, radians, isclose

def rotate_vector(vector: tuple[float, float], angle: float) -> tuple[float, float]:
    rad_angle = radians(angle)
    return (vector[0] * cos(rad_angle) + vector[1] * sin(rad_angle),
            vector[0] * (-sin(rad_angle)) + vector[1] * cos(rad_angle))

    # Assumes screen coordinates - x increasing right, y increasing downwards, positive angle CCW

if __name__ == "__main__":

    assert rotate_vector((1, 1), 0) == (1, 1)
    print(rotate_vector((1, 0), 90))
    print(rotate_vector((0, -1), 90))
    print(rotate_vector((0, -1), 180))
    print(rotate_vector((0, -1), 270))
    assert isclose(rotate_vector((1, 0), 90)[0], (0, -1)[0], abs_tol=1e10)
    print(rotate_vector((1, 0), 90)[0])
    print((0, -1)[0])
    print()

    for n in range(1, 5):
        angle = 360 / n
        anchor_offsets = [rotate_vector((0, -50), i * angle) for i in range(n)]
        print(f"n={n}   {anchor_offsets}")