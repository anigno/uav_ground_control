import matplotlib.pyplot as plt
import random
def draw3d(xa: [], ya: [], za: [], title='Graph3d'):
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection="3d")
    ax.plot3D(xa, ya, za, "blue", linewidth=2)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(title)
    plt.show()

if __name__ == '__main__':
    x = [random.uniform(-3, 3) for _ in range(10)]
    y = [random.uniform(-3, 3) for _ in range(10)]
    z = [random.uniform(-3, 3) for _ in range(10)]

    draw3d(x, y, z)
