from .parse import parse_details


def test_goal_with_no_assists():
    description = "#13 LAMOUREUX Maveric scored for Canada."

    goal = parse_details(description)

    assert (
        goal["goal"]
        == {
            "last": "Lamoureux",
            "first": "Maveric",
            "country": "Canada",
            "number": "13",
        }
        and goal["assists"] == []
    )


def test_goal_with_one_assist():
    description = (
        "#18 PETROVSKY Servac scored for Slovakia (Assisted by #10 MESAR Filip)."
    )

    goal = parse_details(description)

    assert goal["goal"] == {
        "last": "Petrovsky",
        "first": "Servac",
        "country": "Slovakia",
        "number": "18",
    } and goal["assists"][0] == {
        "last": "Mesar",
        "first": "Filip",
        "country": "Slovakia",
        "number": "10",
    }


def test_goal_with_two_assists():
    description = "#4 STRBAK Maxim scored for Slovakia (Assisted by #19 PEKARCIK Juraj and #27 HONZEK Samuel)."

    goal = parse_details(description)

    assert (
        goal["goal"]
        == {"last": "Strbak", "first": "Maxim", "country": "Slovakia", "number": "4"}
        and goal["assists"][0]
        == {"last": "Pekarcik", "first": "Juraj", "country": "Slovakia", "number": "19"}
        and goal["assists"][1]
        == {"last": "Honzek", "first": "Samuel", "country": "Slovakia", "number": "27"}
    )


def test_scorer_with_dash_in_name():
    description = "#4 VITTASMAKI Veli-Matti scored for Finland."

    goal = parse_details(description)

    assert goal["goal"] == {
        "last": "Vittasmaki",
        "first": "Veli-Matti",
        "country": "Finland",
        "number": "4",
    }


def test_da_costa():
    description = "#41 BELLEMARE Pierre-Edouard scored for France (Assisted by #14 da COSTA Stephane)."
    goal = parse_details(description)

    assert goal["assists"][0] == {
        "last": "Costa",
        "first": "Stephane",
        "country": "France",
        "number": "14",
    }
