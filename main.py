import sys
import timeit
import numpy
import road
import river
from numba import njit

from perlin_numpy import (
    generate_fractal_noise_2d
)

import numpy as np
from PIL import Image
from multiprocessing import Process

veg_parts = "./veg_parts/"
land_parts = "./land_parts/"


@njit
def color_loop(world, lakes, roads, rivers, num=-1):
    Sand = [210, 200, 160]
    Water = [0, 138, 255]
    Dirt = [120, 70, 20]
    Light_Grass = [145, 135, 60]
    Medium_Grass = [117, 117, 47]
    Dark_Grass = [90, 100, 35]
    Less_Trees_Dark_Grass = [64, 0, 0]
    Trees_Bush_Dark_Grass = [255, 0, 255]
    Trees_Dark_Grass = [127, 0, 0]
    Trees = [255, 0, 0]
    AllGrass = [0, 255, 0]
    Nothing = [0, 0, 0]
    Dark_Asphalt = [100, 100, 100]
    Dark_Pothole = [110, 100, 100]

    land = np.zeros(world.shape + (3,))
    veg = np.zeros(world.shape + (3,))
    trace = 0
    percent = 0

    for i in range(len(land)):
        trace = trace + 1
        if trace == round(len(land) / 50):
            trace = 0
            percent += 2
        for j in range(len(land)):
            if roads[i][j][0] != 255:
                if np.random.rand() < 0.08:
                    land[i][j] = Dark_Pothole
                else:
                    land[i][j] = Dark_Asphalt
                veg[i][j] = Nothing
            elif rivers[i][j][0] != 255:
                land[i][j] = Water
                veg[i][j] = Nothing
            elif lakes[i][j] > 210:
                land[i][j] = Water
                veg[i][j] = Nothing
            elif lakes[i][j] == 210:
                land[i][j] = Sand
                veg[i][j] = Nothing
            else:
                if world[i][j] < 20:
                    land[i][j] = Dirt
                    veg[i][j] = AllGrass
                elif world[i][j] < 80:
                    veg[i][j] = AllGrass
                    land[i][j] = Light_Grass
                elif world[i][j] < 100:
                    veg[i][j] = AllGrass
                    land[i][j] = Medium_Grass
                elif world[i][j] < 135:
                    veg[i][j] = AllGrass
                    land[i][j] = Dark_Grass
                elif world[i][j] < 140:
                    veg[i][j] = Less_Trees_Dark_Grass
                    land[i][j] = Dark_Grass
                elif world[i][j] < 160:
                    veg[i][j] = Trees_Bush_Dark_Grass
                    land[i][j] = Dark_Grass
                elif world[i][j] < 190:
                    veg[i][j] = Trees_Dark_Grass
                    land[i][j] = Dark_Grass
                else:
                    veg[i][j] = Trees
                    land[i][j] = Dark_Grass
                    if np.random.rand() < 0.5:
                        veg[i][j] = Nothing
                if np.random.rand() < 0.02:
                    veg[i][j] = Nothing
    return land, veg, num


def add_color(world, lakes, roads, rivers, num=-1):
    # print("\r   Coloring Thread " + str(num) + " " + str(percent) + "%", end="   ")
    land, veg, num = color_loop(world, lakes, roads, rivers, num)
    rebuild(land, veg, num)


def rebuild(land, veg, num):
    if num != -1:
        land_img = Image.fromarray(land.astype('uint8'), mode='RGB')
        land_img.save(land_parts + str(num) + ".png")
        Image.fromarray(veg.astype('uint8'), mode='RGB').save(veg_parts + str(num) + ".png")
    else:
        return land, veg


def multiprocess_image(world, lakes, road_array, river_array):
    upper_third = np.hsplit(np.vsplit(world, 3)[0], 3)
    middle_third = np.hsplit(np.vsplit(world, 3)[1], 3)
    lower_third = np.hsplit(np.vsplit(world, 3)[2], 3)

    upper_left = upper_third[0]
    upper_middle = upper_third[1]
    upper_right = upper_third[2]
    middle_left = middle_third[0]
    middle_middle = middle_third[1]
    middle_right = middle_third[2]
    lower_left = lower_third[0]
    lower_middle = lower_third[1]
    lower_right = lower_third[2]

    lake_upper_third = np.hsplit(np.vsplit(lakes, 3)[0], 3)
    lake_middle_third = np.hsplit(np.vsplit(lakes, 3)[1], 3)
    lake_lower_third = np.hsplit(np.vsplit(lakes, 3)[2], 3)

    lake_upper_left = lake_upper_third[0]
    lake_upper_middle = lake_upper_third[1]
    lake_upper_right = lake_upper_third[2]
    lake_middle_left = lake_middle_third[0]
    lake_middle_middle = lake_middle_third[1]
    lake_middle_right = lake_middle_third[2]
    lake_lower_left = lake_lower_third[0]
    lake_lower_middle = lake_lower_third[1]
    lake_lower_right = lake_lower_third[2]

    road_upper_third = np.hsplit(np.vsplit(road_array, 3)[0], 3)
    road_middle_third = np.hsplit(np.vsplit(road_array, 3)[1], 3)
    road_lower_third = np.hsplit(np.vsplit(road_array, 3)[2], 3)

    road_upper_left = road_upper_third[0]
    road_upper_middle = road_upper_third[1]
    road_upper_right = road_upper_third[2]
    road_middle_left = road_middle_third[0]
    road_middle_middle = road_middle_third[1]
    road_middle_right = road_middle_third[2]
    road_lower_left = road_lower_third[0]
    road_lower_middle = road_lower_third[1]
    road_lower_right = road_lower_third[2]

    river_upper_third = np.hsplit(np.vsplit(river_array, 3)[0], 3)
    river_middle_third = np.hsplit(np.vsplit(river_array, 3)[1], 3)
    river_lower_third = np.hsplit(np.vsplit(river_array, 3)[2], 3)

    river_upper_left = river_upper_third[0]
    river_upper_middle = river_upper_third[1]
    river_upper_right = river_upper_third[2]
    river_middle_left = river_middle_third[0]
    river_middle_middle = river_middle_third[1]
    river_middle_right = river_middle_third[2]
    river_lower_left = river_lower_third[0]
    river_lower_middle = river_lower_third[1]
    river_lower_right = river_lower_third[2]

    process_data = [
        (upper_left, lake_upper_left, road_upper_left, river_upper_left, 0,),
        (upper_middle, lake_upper_middle, road_upper_middle, river_upper_middle, 1,),
        (upper_right, lake_upper_right, road_upper_right, river_upper_right, 2,),
        (middle_left, lake_middle_left, road_middle_left, river_middle_left, 3,),
        (middle_middle, lake_middle_middle, road_middle_middle, river_middle_middle, 4,),
        (middle_right, lake_middle_right, road_middle_right, river_middle_right, 5,),
        (lower_left, lake_lower_left, road_lower_left, river_lower_left, 6,),
        (lower_middle, lake_lower_middle, road_lower_middle, river_lower_middle, 7,),
        (lower_right, lake_lower_right, road_lower_right, river_lower_right, 8,)
    ]

    processes = []

    for each in process_data:
        processes.append(Process(target=add_color, args=each))

    for p in processes:
        p.start()
    for p in processes:
        p.join()


def main(width=5):
    BLOCK_WIDTH = width
    SIZE = BLOCK_WIDTH * 300
    SHAPE = (SIZE, SIZE)
    SCALE = (round(SIZE / 100), round(SIZE / 100))

    start = timeit.default_timer()
    print(
        "\rGenerating a world " + str(BLOCK_WIDTH) + "*" + str(BLOCK_WIDTH) + " size.  " + str(SIZE * SIZE) + " pixels")

    partial_start = timeit.default_timer()
    print("\r Generating world perlin... ", end="")
    world_perlin = generate_fractal_noise_2d(SHAPE, SCALE, octaves=3, persistence=0.5, lacunarity=2)
    partial_stop = timeit.default_timer()
    print('Time: ', "{:.2f}".format(partial_stop - partial_start), end="\n")

    partial_start = timeit.default_timer()
    print("\r Generating lakes perlin... ", end="")
    lake_perlin = generate_fractal_noise_2d(SHAPE, SCALE, persistence=0.5, lacunarity=2)
    partial_stop = timeit.default_timer()
    print('Time: ', "{:.2f}".format(partial_stop - partial_start), end="\n")

    partial_start = timeit.default_timer()
    print("\r Generating roads...        ", end="")
    road.generate(SIZE)
    road_img = Image.open("./data/road_img.png")
    road_array = numpy.array(road_img)
    partial_stop = timeit.default_timer()
    print('Time: ', "{:.2f}".format(partial_stop - partial_start), end="\n")

    partial_start = timeit.default_timer()
    print("\r Generating rivers...       ", end="")
    river.generate(SIZE)
    river_img = Image.open("./data/river_img.png")
    river_array = numpy.array(river_img)
    partial_stop = timeit.default_timer()
    print('Time: ', "{:.2f}".format(partial_stop - partial_start), end="\n")

    partial_start = timeit.default_timer()
    print("\r Coloring...                ", end="")
    lake_img = Image.fromarray(lake_perlin)
    lake_img.save("./data/lakes.png")

    multiprocess_image(world_perlin, lake_perlin, road_array, river_array)
    rebuild_images(SIZE)
    partial_stop = timeit.default_timer()
    print('Time: ', "{:.2f}".format(partial_stop - partial_start), end="\n")

    stop = timeit.default_timer()
    print('Overall time: ', "{:.2f}".format(stop - start), end="\n")

    # (full_land, full_veg) = add_color(world, lakes)
    # Image.fromarray(full_veg.astype('uint8'), mode='RGB').save("rptown_veg_full.png")


def rebuild_images(SIZE):
    veg_images = []
    world_images = []
    for i in range(9):
        veg_images.append(Image.open(veg_parts + str(i) + ".png"))
        world_images.append(Image.open(land_parts + str(i) + ".png"))
    new_veg_image = Image.new('RGB', (SIZE, SIZE), (250, 250, 250))
    new_world_image = Image.new('RGB', (SIZE, SIZE), (250, 250, 250))

    for j in range(3):
        for k in range(3):
            new_veg_image.paste(veg_images[j * 3 + k], (int(SIZE / 3 * k), int(SIZE / 3 * j)))
            new_world_image.paste(world_images[j * 3 + k], (int(SIZE / 3 * k), int(SIZE / 3 * j)))
    new_veg_image.save("rptown_veg.png", "PNG")
    new_world_image.save("rptown.png", "PNG")


if __name__ == '__main__':
    args = sys.argv
    try:
        arg_last = int(args[len(args) - 1])
        if arg_last > 0:
            BLOCK_WIDTH = arg_last
            main(BLOCK_WIDTH)
        else:
            raise AssertionError
    except ValueError:
        print("Last argument must be map width in blocks. A block is a 300x300 pixel region.")
    except AssertionError:
        print("A map has to be at least 1 block wide.")

    # test()
