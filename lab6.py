
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Slider, Button
import numpy as np

def create_letter_K():
    vertices = [
        [1, 1, 0], [1, 6, 0], [2,1,0], [2,6,0],[2,3,0],[2,4,0],[4,1,0],[5,1,0],[4,6,0],[5,6,0],
        [1,1,1],[1,6,1],[2,1,1],[2,6,1],[2,3,1],[2,4,1],[4,1,1],[5,1,1],[4,6,1],[5,6,1]
    ]

    faces = [
       [0,1,3,2],[4,5,7,6],[5,4,9,8],[10,11,13,12], [14,15,17,16],[15,14,19,18],[0,10,11,1],
        [1, 3,11,13], [13,3,5,15], [5,15,18,8],[8,18,19,9],[19,9,4,14],[5,15,17,7],[7,17,16,6],[16,6,4,14],[14,4,2,12],
        [12,2,0,10]
    ]

    return np.array(vertices), faces

def plot_3d_object(ax, vertices, faces):
    ax.clear()
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.set_xlim(-5, 10)
    ax.set_ylim(-5, 10)
    ax.set_zlim(-5, 10)

    poly3d = [[vertices[vert_id] for vert_id in face] for face in faces]
    ax.add_collection3d(Poly3DCollection(poly3d, alpha=0.5, edgecolor='k'))

    for vert in vertices:
        ax.scatter(*vert, color="r", s=50)

    plt.draw()

def plot_projection(ax, vertices, plane):
    ax.clear()
    if plane == 'xy':
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.scatter(vertices[:, 0], vertices[:, 1], color="b", s=50)
        for edge in faces:
            xy = vertices[edge][:, :2]
            ax.plot(xy[:, 0], xy[:, 1], color="k")
    elif plane == 'xz':
        ax.set_xlabel("X")
        ax.set_ylabel("Z")
        ax.scatter(vertices[:, 0], vertices[:, 2], color="b", s=50)
        for edge in faces:
            xz = vertices[edge][:, [0, 2]]
            ax.plot(xz[:, 0], xz[:, 1], color="k")
    elif plane == 'yz':
        ax.set_xlabel("Y")
        ax.set_ylabel("Z")
        ax.scatter(vertices[:, 1], vertices[:, 2], color="b", s=50)
        for edge in faces:
            yz = vertices[edge][:, 1:]
            ax.plot(yz[:, 0], yz[:, 1], color="k")

    ax.set_xlim(-5, 10)
    ax.set_ylim(-5, 10)
    plt.draw()

def apply_transformation(vertices, transformation_matrix):
    homogenous_vertices = np.hstack([vertices, np.ones((vertices.shape[0], 1))])
    transformed_vertices = homogenous_vertices @ transformation_matrix.T
    return transformed_vertices[:, :3]

def create_scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def create_translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def create_rotation_matrix(axis, angle):
    angle = np.radians(angle)
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c = np.cos(angle)
    s = np.sin(angle)
    t = 1 - c

    return np.array([
        [t*x*x + c,   t*x*y - s*z, t*x*z + s*y, 0],
        [t*x*y + s*z, t*y*y + c,   t*y*z - s*x, 0],
        [t*x*z - s*y, t*y*z + s*x, t*z*z + c,   0],
        [0,           0,           0,           1]
    ])

def update(val):
    global vertices

    sx = scale_x_slider.val
    sy = scale_y_slider.val
    sz = scale_z_slider.val

    tx = translate_x_slider.val
    ty = translate_y_slider.val
    tz = translate_z_slider.val

    angle = rotate_slider.val
    axis_x = rotate_axis_x_slider.val
    axis_y = rotate_axis_y_slider.val
    axis_z = rotate_axis_z_slider.val

    scale_matrix = create_scale_matrix(sx, sy, sz)
    translation_matrix = create_translation_matrix(tx, ty, tz)
    rotation_axis = np.array([axis_x, axis_y, axis_z])
    rotation_matrix = create_rotation_matrix(rotation_axis, angle)

    final_matrix = scale_matrix @ translation_matrix @ rotation_matrix

    print("Final Transformation Matrix:")
    print(final_matrix)

    transformed_vertices = apply_transformation(vertices, final_matrix)
    plot_3d_object(ax_3d, transformed_vertices, faces)
    plot_projection(ax_xy, transformed_vertices, 'xy')
    plot_projection(ax_xz, transformed_vertices, 'xz')
    plot_projection(ax_yz, transformed_vertices, 'yz')
    if name == "main":
        vertices, faces = create_letter_K()

        fig = plt.figure(figsize=(18, 12))

        ax_3d = fig.add_subplot(231, projection='3d')
        ax_3d.set_title("3D View")

        ax_xy = fig.add_subplot(232)
        ax_xy.set_title("Projection on XY Plane")

        ax_xz = fig.add_subplot(233)
        ax_xz.set_title("Projection on XZ Plane")

        ax_yz = fig.add_subplot(234)
        ax_yz.set_title("Projection on YZ Plane")

        plot_3d_object(ax_3d, vertices, faces)
        plot_projection(ax_xy, vertices, 'xy')
        plot_projection(ax_xz, vertices, 'xz')
        plot_projection(ax_yz, vertices, 'yz')

        slider_width = 0.2
        slider_height = 0.01
        slider_start_x = 0.75
        slider_y_spacing = 0.02

        ax_scale_x = plt.axes([slider_start_x, 0.12, slider_width, slider_height])
        ax_scale_y = plt.axes([slider_start_x, 0.12 + slider_y_spacing, slider_width, slider_height])
        ax_scale_z = plt.axes([slider_start_x, 0.12 + 2 * slider_y_spacing, slider_width, slider_height])

        ax_translate_x = plt.axes([slider_start_x, 0.12 + 3 * slider_y_spacing, slider_width, slider_height])
        ax_translate_y = plt.axes([slider_start_x, 0.12 + 4 * slider_y_spacing, slider_width, slider_height])
        ax_translate_z = plt.axes([slider_start_x, 0.12 + 5 * slider_y_spacing, slider_width, slider_height])

        ax_rotate = plt.axes([slider_start_x, 0.12 + 6 * slider_y_spacing, slider_width, slider_height])
        ax_rotate_axis_x = plt.axes([slider_start_x, 0.12 + 7 * slider_y_spacing, slider_width, slider_height])
        ax_rotate_axis_y = plt.axes([slider_start_x, 0.12 + 8 * slider_y_spacing, slider_width, slider_height])
        ax_rotate_axis_z = plt.axes([slider_start_x, 0.12 + 9 * slider_y_spacing, slider_width, slider_height])

        scale_x_slider = Slider(ax_scale_x, 'Scale X', 0.5, 2.0, valinit=1.0)
        scale_y_slider = Slider(ax_scale_y, 'Scale Y', 0.5, 2.0, valinit=1.0)
        scale_z_slider = Slider(ax_scale_z, 'Scale Z', 0.5, 2.0, valinit=1.0)

        translate_x_slider = Slider(ax_translate_x, 'Translate X', -5, 5, valinit=0)
        translate_y_slider = Slider(ax_translate_y, 'Translate Y', -5, 5, valinit=0)
        translate_z_slider = Slider(ax_translate_z, 'Translate Z', -5, 5, valinit=0)

        rotate_slider = Slider(ax_rotate, 'Rotate Angle', 0, 360, valinit=0)
        rotate_axis_x_slider = Slider(ax_rotate_axis_x, 'Rotate Axis X', -1, 1, valinit=1)
        rotate_axis_y_slider = Slider(ax_rotate_axis_y, 'Rotate Axis Y', -1, 1, valinit=0)
        rotate_axis_z_slider = Slider(ax_rotate_axis_z, 'Rotate Axis Z', -1, 1, valinit=0)

        scale_x_slider.on_changed(update)
        scale_y_slider.on_changed(update)
        scale_z_slider.on_changed(update)
        translate_x_slider.on_changed(update)
        translate_y_slider.on_changed(update)
        translate_z_slider.on_changed(update)
        rotate_slider.on_changed(update)
        rotate_axis_x_slider.on_changed(update)
        rotate_axis_y_slider.on_changed(update)
        rotate_axis_z_slider.on_changed(update)

        plt.show()