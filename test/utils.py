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


def compare_history(orders, history_orders_after_confirmation):
    assert len(orders) == len(history_orders_after_confirmation)
    for i, order in enumerate(orders):
        expected_order = history_orders_after_confirmation[i]
        assert expected_order.shipping_address == order.shipping_address
        assert order.shipping_address == expected_order.shipping_address
        compare_items(order.items, expected_order.items)
