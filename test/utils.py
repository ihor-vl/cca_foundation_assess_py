def compare_items(items_under_test, expected_items):

    assert len(items_under_test) == len(expected_items)
    for item in items_under_test:
        expected_item = next(
            (expected_item for expected_item in expected_items
             if expected_item.product.id == item.product.id),
            False
        )
        assert expected_item
        assert item.quantity == expected_item.quantity
        assert item.product.id == expected_item.product.id
        assert item.product.description == expected_item.product.description
        assert item.product.price == expected_item.product.price
