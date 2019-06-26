from agent import PiranhasAgent


def test_distance():
    p1 = (4, 3)
    p2 = (0, 2)
    center = (4.5, 4.5)
    p1Distance = PiranhasAgent.distanceScore(p1, center)
    p2Distance = PiranhasAgent.distanceScore(p2, center)
    assert p1Distance < p2Distance

def test_center():
    fish = [(0, 1), (0, 2), (0, 3), (4, 1), (4, 2), (4, 3)]
    center = PiranhasAgent.fishCenter(fish)
    assert center == (2, 2)

# -*- encoding: utf-8-unix -*-
