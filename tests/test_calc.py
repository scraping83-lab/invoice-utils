import pytest

from invoice_utils import format_currency, subtotal, tax, total


@pytest.mark.parametrize(
    "lines, expected",
    [
        ([(1, 10.00)], 10.00),
        ([(2, 19.99)], 39.98),
        ([(1, 10.00), (3, 2.50)], 17.50),
        ([], 0),
        ([(5, 0.01)], 0.05),
    ],
)
def test_subtotal(lines, expected):
    assert subtotal(lines) == expected


def test_subtotal_rejects_negative_quantity():
    with pytest.raises(ValueError, match="quantity cannot be negative"):
        subtotal([(-1, 10.00)])


def test_subtotal_rejects_negative_price():
    with pytest.raises(ValueError, match="unit_price cannot be negative"):
        subtotal([(1, -10.00)])


def test_tax_default_rate():
    assert tax(100.00) == 8.75


def test_tax_custom_rate():
    assert tax(100.00, rate=0.10) == 10.00


def test_tax_rounding():
    assert tax(10.00) == 0.88


def test_total_includes_tax():
    assert total([(1, 100.00)]) == 108.75


@pytest.fixture
def sample_lines():
    return [(2, 15.00), (1, 7.50)]


def test_total_sample_invoice(sample_lines):
    # subtotal 37.50, tax 3.28
    assert total(sample_lines) == 40.78


@pytest.mark.parametrize(
    "amount, expected",
    [
        (1234.5, "$1,234.50"),
        (0, "$0.00"),
        (-42.1, "$-42.10"),
        (1000000, "$1,000,000.00"),
    ],
)
def test_format_currency(amount, expected):
    assert format_currency(amount) == expected
