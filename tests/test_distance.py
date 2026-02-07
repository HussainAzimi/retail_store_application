from northstar.distance import Euclidean, Manhattan, GreatCircle

def test_distance_strategies():
    e = Euclidean().between((0.0,0.0),(3.0,4.0))
    m = Manhattan().between((0.0,0.0),(3.0,4.0))
    assert round(e,6) == 5.0
    assert round(m,6) == 7.0
    gc = GreatCircle().between((0.0,0.0),(0.0,1.0))
    assert 110.0 < gc < 112.5  # ~111.32 km along equator
