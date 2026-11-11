from core.pattern import route_and_complete


def test_simple_uses_fast():
    r = route_and_complete("warranty?")
    assert "[fast]" in r.text


def test_complex_uses_capable():
    r = route_and_complete(" ".join(["help"] * 20))
    assert "[capable]" in r.text
