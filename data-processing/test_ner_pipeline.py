from ner_pipeline import generate_title_searchindex
from os.path import dirname, join
import pandas as pd

# Setup test environment
current_dir = dirname(__file__)
test_sample = pd.read_csv(join(current_dir, "./testsample_policereports.csv"))
search_index = generate_title_searchindex(test_sample)


def test_title_location_detection():
    assert (
        len(search_index["LocationsFromNER"][0]) == 0
    ), "Location detected in title without locations"
    assert (
        len(search_index["LocationsFromNER"][1]) == 0
    ), "Location detected in title without locations"
    assert (
        len(search_index["LocationsFromNER"][2]) == 1
    ), "Location not detected in title"
    assert (
        len(search_index["LocationsFromNER"][3]) == 1
    ), "Location not detected in title"
    assert (
        len(search_index["LocationsFromNER"][4]) == 0
    ), "Location detected in title without locations"

    assert search_index["LocationsFromNER"][2] == {
        ("Wilmersdorfer Straße")
    }, "Wrong location detected"
    assert search_index["LocationsFromNER"][2] == {
        ("Tempelhof")
    }, "Wrong location detected"


def test_title_indexing():
    assert search_index["LocationsOffsets"][2][0] == 16, "Wrong location index"
    assert search_index["LocationsOffsets"][3][0] == 9, "Wrong location index"
