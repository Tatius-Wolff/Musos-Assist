import pytest
from musos_assist.insights import Gender, AgeRange, TopLocation, Audience


def test_gender_float_float() -> None:
    class_under_test = Gender(male=89.2, female=9.2)
    assert class_under_test.male == 89.2
    assert class_under_test.female == 9.2

    expected_message = "male=89.2 female=9.2 other=1.6"
    actual_message = str(class_under_test)

    assert expected_message in actual_message


def test_gender_float_float_float() -> None:
    class_under_test = Gender(male=89.2, female=9.2, other=1.6)
    assert class_under_test.male == 89.2
    assert class_under_test.female == 9.2
    assert class_under_test.other == 1.6

    expected_message = "male=89.2 female=9.2 other=1.6"
    actual_message = str(class_under_test)

    assert expected_message in actual_message


def test_gender_invalid_total() -> None:
    with pytest.raises(ValueError) as excinfo:
        Gender(male=20.0, female=20.0, other=20.0)

    expected_message = "Total percentage [20.0] + [20.0] + [20.0] does not equal 100%."
    actual_message = str(excinfo.value)

    assert expected_message in actual_message


def test_gender_invalid_param() -> None:
    with pytest.raises(ValueError) as excinfo:
        Gender(male=-20.0, female=120.0)

    expected_message = "Parameter [male]: [-20.0] is not between [0.0] and [100.0]."
    actual_message = str(excinfo.value)

    assert expected_message in actual_message


def test_age_range() -> None:
    class_under_test = AgeRange(min_age=18, max_age=24, percent=13.0)
    assert class_under_test.min_age == 18
    assert class_under_test.max_age == 24
    assert class_under_test.percent == 13.0

    expected_message = "min_age=18 max_age=24 percent=13.0"
    actual_message = str(class_under_test)

    assert expected_message in actual_message


def test_age_range_no_max() -> None:
    class_under_test = AgeRange(min_age=100, percent=13.0)
    assert class_under_test.min_age == 100
    assert class_under_test.max_age == 150
    assert class_under_test.percent == 13.0

    expected_message = "min_age=100 max_age=150 percent=13.0"
    actual_message = str(class_under_test)

    assert expected_message in actual_message


def test_age_range_invalid_min_age() -> None:
    with pytest.raises(ValueError) as excinfo:
        AgeRange(min_age=-1, max_age=24, percent=13.0)

    expected_message = "Parameter [min_age]: [-1] is not between [0] and [150]."
    actual_message = str(excinfo.value)

    assert expected_message in actual_message


def test_age_range_invalid_max_age() -> None:
    with pytest.raises(ValueError) as excinfo:
        AgeRange(min_age=18, max_age=151, percent=13.0)

    expected_message = "Parameter [max_age]: [151] is not between [0] and [150]."
    actual_message = str(excinfo.value)

    assert expected_message in actual_message


def test_age_range_invalid_percentage() -> None:
    with pytest.raises(ValueError) as excinfo:
        AgeRange(min_age=18, max_age=24, percent=101.0)

    expected_message = "Parameter [percent]: [101.0] is not between [0.0] and [100.0]."
    actual_message = str(excinfo.value)

    assert expected_message in actual_message


def test_top_location() -> None:
    class_under_test = TopLocation(location="New South Wales", percent=43.4)
    assert class_under_test.location == "New South Wales"
    assert class_under_test.percent == 43.4

    expected_message = "location='New South Wales' percent=43.4"
    actual_message = str(class_under_test)

    assert expected_message in actual_message


def test_top_location_invalid_percentage() -> None:
    with pytest.raises(ValueError) as excinfo:
        TopLocation(location="New South Wales", percent=101.0)

    expected_message = "Parameter [percent]: [101.0] is not between [0.0] and [100.0]."
    actual_message = str(excinfo.value)

    assert expected_message in actual_message


def test_audience() -> None:
    g = Gender(male=89.2, female=9.2)
    ar0 = AgeRange(min_age=18, max_age=24, percent=13.0)
    ar1 = AgeRange(min_age=25, max_age=34, percent=24.0)
    ar2 = AgeRange(min_age=35, max_age=44, percent=25.1)
    ar3 = AgeRange(min_age=45, max_age=54, percent=18.7)
    ar4 = AgeRange(min_age=55, max_age=64, percent=11.6)
    ar5 = AgeRange(min_age=65, percent=24.0)  # using the optional max_age constructor
    ar = [ar0, ar1, ar2, ar3, ar4, ar5]
    tl1 = TopLocation(location="New South Wales", percent=43.4)
    tl2 = TopLocation(location="Victoria", percent=24.5)
    tl3 = TopLocation(location="Queensland", percent=15.8)
    tl4 = TopLocation(location="Western Australia", percent=7.8)
    tl5 = TopLocation(location="South Australia", percent=4.3)
    tl = [tl1, tl2, tl3, tl4, tl5]
    class_under_test = Audience(gender=g, agerange=ar, toplocation=tl)

    expected_message = "male=89.2 female=9.2 other=1.6"
    actual_message = str(class_under_test.gender)
    assert expected_message in actual_message

    expected_message = "min_age=18 max_age=24 percent=13.0"
    actual_message = str(class_under_test.agerange[0])
    assert expected_message in actual_message

    expected_message = "location='New South Wales' percent=43.4"
    actual_message = str(class_under_test.toplocation[0])
    assert expected_message in actual_message

    expected_message = "gender=Gender(male=89.2, female=9.2, other=1.6) agerange=[AgeRange(min_age=18, max_age=24, \
percent=13.0), AgeRange(min_age=25, max_age=34, percent=24.0), AgeRange(min_age=35, max_age=44, \
percent=25.1), AgeRange(min_age=45, max_age=54, percent=18.7), AgeRange(min_age=55, max_age=64, percent=11.6), \
AgeRange(min_age=65, max_age=150, percent=24.0)] toplocation=[TopLocation(location='New South Wales', \
percent=43.4), TopLocation(location='Victoria', percent=24.5), TopLocation(location='Queensland', \
percent=15.8), TopLocation(location='Western Australia', percent=7.8), TopLocation(location='South Australia', \
percent=4.3)]"
    actual_message = str(class_under_test)
    assert expected_message in actual_message
