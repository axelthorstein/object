from object.product import Product


def test_product_check_similar_exact_values():
    code = '020202030303040404050505000000010101'
    product_map = {'020202030303040404050505000000010101': 'test-object'}
    expected = ('020202030303040404050505000000010101', 1)
    actual = tuple(Product.check_similar(code, product_map))

    assert expected == actual


def test_product_check_similar_almost_exact_values():
    code = '020202030303040404050505000000010111'
    product_map = {'020202030303040404050505000000010101': 'test-object'}
    expected = ('020202030303040404050505000000010101', 0.97)
    actual = tuple(Product.check_similar(code, product_map))

    assert expected == actual


def test_product_check_similar_90_percent_similar():
    code = '020202030303040404050505000000010999'
    product_map = {'020202030303040404050505000000010101': 'test-object'}
    expected = ('020202030303040404050505000000010101', 0.92)
    actual = tuple(Product.check_similar(code, product_map))

    assert expected == actual


def test_product_check_similar_80_percent_similar():
    code = '020202030303040404050505000000999999'
    product_map = {'020202030303040404050505000000010101': 'test-object'}
    expected = (None, 0.83)
    actual = tuple(Product.check_similar(code, product_map))

    assert expected == actual


def test_product_check_similar_79_percent_similar():
    code = '020202030303040404050505000099999999'
    product_map = {'020202030303040404050505000000010101': 'test-object'}
    expected = (None, 0.78)
    actual = tuple(Product.check_similar(code, product_map))

    assert expected == actual


def test_product_check_similar_different_values():
    code = '999999999999999999999999999999999999'
    product_map = {'020202030303040404050505000000010101': 'test-object'}
    expected = (None, 0.0)
    actual = tuple(Product.check_similar(code, product_map))

    assert expected == actual
