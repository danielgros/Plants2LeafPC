import csv
import math
import pickle
import cv2
import numpy as np
import sys


def getMaxDegrees(reader):
    max_x_degree, min_x_degree, max_y_degree, min_y_degree = (
        -math.inf,
        math.inf,
        -math.inf,
        math.inf,
    )

    first_line = True
    for lines in reader:
        if first_line:
            first_line = False
            continue
        x_coord = float(lines[0])
        y_coord = float(lines[1])
        z_coord = float(lines[2])
        # r = int(lines[3])
        # g = int(lines[4])
        # b = int(lines[5])
        # a = int(lines[6])
        x_degrees = math.degrees(math.atan(x_coord / z_coord))
        y_degrees = math.degrees(math.atan(y_coord / z_coord))

        if x_degrees > max_x_degree:
            max_x_degree = x_degrees
        if x_degrees < min_x_degree:
            min_x_degree = x_degrees
        if y_degrees > max_y_degree:
            max_y_degree = y_degrees
        if y_degrees < min_y_degree:
            min_y_degree = y_degrees

    return [max_x_degree, min_x_degree, max_y_degree, min_y_degree]


def anglesToIndex(
    x_degree,
    y_degree,
    width,
    height,
    max_x_degree,
    min_x_degree,
    max_y_degree,
    min_y_degree,
):
    x_interval = (max_x_degree + abs(min_x_degree)) / width
    y_interval = (max_y_degree + abs(min_y_degree)) / height
    x_shifted = x_degree + ((max_x_degree + abs(min_x_degree)) / 2)
    if x_shifted < 0:
        print("x negative")
        x_shifted = -1
    y_shifted = y_degree + ((max_y_degree + abs(min_y_degree)) / 2)
    if y_shifted < 0:
        print("y negative")
        y_shifted = -1
    x_pos = (x_shifted) / x_interval
    y_pos = (y_shifted) / y_interval
    if x_pos > width - 1:
        print("x too big")
        x_pos = -1
    if y_pos > height - 1:
        print("y too big")
        y_pos = -1
    return int(x_pos), int(y_pos)


def anglesToIndexLoop(
    reader,
    img,
    point_cloud,
    overlap,
    width,
    height,
    max_x_degree,
    min_x_degree,
    max_y_degree,
    min_y_degree,
):
    first_line = True
    for lines in reader:
        if first_line:
            first_line = False
            continue
        x_coord = float(lines[0])
        y_coord = float(lines[1])
        z_coord = float(lines[2])
        r = int(lines[3])
        g = int(lines[4])
        b = int(lines[5])
        x_degrees = math.degrees(math.atan(x_coord / z_coord))
        y_degrees = math.degrees(math.atan(y_coord / z_coord))
        x_pos, y_pos = anglesToIndex(
            x_degrees,
            y_degrees,
            width,
            height,
            max_x_degree,
            min_x_degree,
            max_y_degree,
            min_y_degree,
        )
        if x_pos == -1 or y_pos == -1:
            continue
        img[y_pos, x_pos, 0] += r
        img[y_pos, x_pos, 1] += g
        img[y_pos, x_pos, 2] += b
        point_cloud[y_pos, x_pos].append(lines)
        overlap[y_pos, x_pos] += 1


def removeVerticalBlackLines(img):
    width = np.shape(img)[1]
    height = np.shape(img)[0]
    black_columb_idx_list = {}
    for c in range(1, width - 1):
        if img[0, c, 0] == 0 and img[0, c, 1] == 0 and img[0, c, 2] == 0:
            isBlackLine = True
            for r in range(0, height):
                if img[r, c, 0] != 0 or img[r, c, 1] != 0 or img[r, c, 2] != 0:
                    isBlackLine = False
                    break
            if isBlackLine:
                black_columb_idx_list[c] = True
    new_img = np.zeros([height, width - len(black_columb_idx_list.keys()), 3])
    cur_col = 0
    for c in range(0, width):
        if c in black_columb_idx_list:
            pass
        else:
            new_img[:, cur_col, :] = img[:, c, :]
            cur_col += 1
    return new_img


def removeHorizontalBlackLines(img):
    width = np.shape(img)[1]
    height = np.shape(img)[0]
    black_row_idx_list = {}
    for r in range(1, height - 1):
        if img[r, 0, 0] == 0 and img[r, 0, 1] == 0 and img[r, 0, 2] == 0:
            isBlackLine = True
            for c in range(0, width):
                if img[r, c, 0] != 0 or img[r, c, 1] != 0 or img[r, c, 2] != 0:
                    isBlackLine = False
                    break
            if isBlackLine:
                black_row_idx_list[r] = True
    new_img = np.zeros([height - len(black_row_idx_list.keys()), width, 3])
    cur_row = 0
    for r in range(0, height):
        if r in black_row_idx_list:
            pass
        else:
            new_img[cur_row, :, :] = img[r, :, :]
            cur_row += 1
    return new_img


def removeVerticalBlackLinesPC(point_cloud):
    width = np.shape(point_cloud)[1]
    height = np.shape(point_cloud)[0]
    black_columb_idx_list = {}
    for c in range(1, width - 1):
        if not point_cloud[0, c]:
            isBlackLine = True
            for r in range(0, height):
                if point_cloud[r, c]:
                    isBlackLine = False
                    break
            if isBlackLine:
                black_columb_idx_list[c] = True
    new_point_cloud = np.empty((height, width - len(black_columb_idx_list.keys())), dtype=object)
    cur_col = 0
    for c in range(0, width):
        if c in black_columb_idx_list:
            pass
        else:
            for r in range(0, height):
                new_point_cloud[r, cur_col] = point_cloud[r, c]
            cur_col += 1
    return new_point_cloud

def removeHorizontalBlackLinesPC(point_cloud):
    width = np.shape(point_cloud)[1]
    height = np.shape(point_cloud)[0]
    black_row_idx_list = {}
    for r in range(1, height - 1):
        if not point_cloud[r, 0]:
            isBlackLine = True
            for c in range(0, width):
                if point_cloud[r, c]:
                    isBlackLine = False
                    break
            if isBlackLine:
                black_row_idx_list[r] = True
    new_point_cloud = np.empty((height - len(black_row_idx_list.keys()), width), dtype=object)
    cur_row = 0
    for r in range(0, height):
        if r in black_row_idx_list:
            pass
        else:
            for c in range(0, width):
                new_point_cloud[cur_row, c] = point_cloud[r, c]
            cur_row += 1
    return new_point_cloud


def pointCloudToImage():

    if len(sys.argv) != 5:
        print("Usage: python3 project_point_cloud_to_2d.py <left_image_path> <point_cloud_path> <projected_image_path> <projected_image_data_path>")
        sys.exit(1)

    left_image_path = sys.argv[1]
    point_cloud_path = sys.argv[2]
    projected_image_path = sys.argv[3]
    projected_image_data_path = sys.argv[4]


    # Suppress the 'no-member' error for cv2.imread
    # pylint: disable=no-member
    left_image = cv2.imread(left_image_path)
    height, width, _ = left_image.shape
    img = np.zeros([height, width, 3])
    point_cloud = np.empty((height, width), dtype=object)
    for i in range(height):
        for j in range(width):
            point_cloud[i, j] = []
    overlap = np.zeros([height, width])
    with open(
        point_cloud_path, mode="r"
    ) as file:
        reader = csv.reader(file)
        max_x_degree, min_x_degree, max_y_degree, min_y_degree = getMaxDegrees(reader)
    with open(
        point_cloud_path, mode="r"
    ) as file:
        reader = csv.reader(file)

        anglesToIndexLoop(
            reader,
            img,
            point_cloud,
            overlap,
            width,
            height,
            max_x_degree,
            min_x_degree,
            max_y_degree,
            min_y_degree,
        )

    for r in range(0, height):
        for c in range(0, width):
            if overlap[r, c] > 1:
                print("there's an overlap", r, c)
                img[r, c, 0] /= overlap[r, c]
                img[r, c, 1] /= overlap[r, c]
                img[r, c, 2] /= overlap[r, c]

    img = removeVerticalBlackLines(img)
    img = removeHorizontalBlackLines(img)

    point_cloud = removeVerticalBlackLinesPC(point_cloud)
    point_cloud = removeHorizontalBlackLinesPC(point_cloud)

    assert img.shape[0] == point_cloud.shape[0]
    assert img.shape[1] == point_cloud.shape[1]

    # fix black lines in different columns FOR LATER
    # img = removeVerticalBlackLines2(img)
    # img = removeHorizontalBlackLines2(img)

    # Suppress the 'no-member' error for cv2.imwrite
    # pylint: disable=no-member
    cv2.imwrite(projected_image_path, img)

    output_filename = projected_image_data_path

    with open(output_filename, "wb") as f:
        pickle.dump(point_cloud, f)


if __name__ == "__main__":
    pointCloudToImage()
