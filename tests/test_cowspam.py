from cowspam import COWSAY_CHARS, Cow, run_kilobytes

def test_cow_init():
    cow = Cow(name="Bessie")
    assert cow.name == "Bessie"
    assert isinstance(cow.age, int)
    assert isinstance(cow.is_normal_cow, bool)
    if not cow.is_normal_cow:
        assert cow._rare_char in COWSAY_CHARS
    else:
        assert cow._rare_char is None

def test_moo():
    c = Cow()
    c.moo()

def test_cow_speak():
    c = Cow()
    c.speak("Hello, world!")

def test_cow_preserves_values():
    c = Cow(name="Betsy", age=5)
    assert c.name == "Betsy"
    assert c.age == 5

def test_kb_produced_small():
    (output_counter, output_kb) = run_kilobytes(1, False)
    assert output_counter.total() <= 5
    assert output_kb >= 1024

def test_kb_produced_large():
    (output_counter, output_kb) = run_kilobytes(2000, False) # 2 MB
    assert output_counter.total() <= 7000
    assert output_kb >= 10240

def test_rare_moo():
    c = Cow(is_normal_cow=False)
    c.moo()
    assert c.moo_text() == c._render("Moo?", c._title)

def test_normal_only():
    for _ in range(5000):
        c = Cow(is_normal_cow=True)
        assert c._rare_char is None

def test_normal_only_kb():
    (output_counter, _) = run_kilobytes(2, False, True)
    assert output_counter["Anomalous Cows"] == 0
