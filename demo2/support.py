import pygame, sys
import math
import numpy as np
from os import walk

def euclidian_distance(player,enemy):
    return math.dist([player.center[0],player.center[1]],[enemy.x,enemy.y])
