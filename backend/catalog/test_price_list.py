import pytest
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APIClient

from catalog.models import Category, Product, Variant
from orders.models import Courier

CSV = """code,name,category,unit,mrp,offer_price
1,2 3/4 Kuruvi,Single Sound Crackers,PKT,99.00,19.80
2,Red Bijili 50 pcs,Bijili Crackers,PKT,176.00,35.20
3,Colour Koti,Flower Pot,Box,2420.00,484.00
"""


@pytest.fixture(autouse=True)
def media(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"


@pytest.fixture
def price_list(tmp_path):
    path = tmp_path / "prices.csv"
    path.write_text(CSV)
    return path


def test_import_makes_shelves_and_products_at_offer_price(price_list, db):
    call_command("import_price_list", str(price_list), stock=20)
    assert list(Category.objects.values_list("name", flat=True)) == ["Single Sound Crackers", "Bijili Crackers", "Flower Pot"]
    v = Variant.objects.get(sku="AK-003")
    assert (v.product.name, v.product.category.name, v.size) == ("Colour Koti", "Flower Pot", "1 Box")
    assert (str(v.price), str(v.mrp), v.stock) == ("484.00", "2420.00", 20)
    assert v.product.description == "Code 3 · per box · 80% off MRP"
    # Each product gets its shelf's picture when the art exists.
    assert Product.objects.get(name="2 3/4 Kuruvi").images.get().image.name == "products/art/single-sound-crackers.jpg"


def test_running_it_again_updates_prices_but_keeps_stock(price_list, db):
    call_command("import_price_list", str(price_list), stock=20)
    Variant.objects.filter(sku="AK-001").update(stock=7)  # some sold
    price_list.write_text(CSV.replace("1,2 3/4 Kuruvi,Single Sound Crackers,PKT,99.00,19.80",
                                      "1,2 3/4 Kuruvi,Single Sound Crackers,PKT,110.00,22.00"))
    call_command("import_price_list", str(price_list), stock=20)
    v = Variant.objects.get(sku="AK-001")
    assert (str(v.price), str(v.mrp), v.stock) == ("22.00", "110.00", 7)
    assert Product.objects.count() == 3 and v.product.images.count() == 1


def test_replace_clears_the_old_catalog_and_couriers_that_do_not_carry_fireworks(price_list, db):
    old = Category.objects.create(name="Pantry")
    Product.objects.create(name="Filter coffee", category=old)
    call_command("import_price_list", str(price_list), replace=True)
    assert not Product.objects.filter(name="Filter coffee").exists() and not Category.objects.filter(name="Pantry").exists()
    assert not Courier.objects.filter(name="DHL", is_active=True).exists()


def test_pages_never_skip_or_repeat_products_added_at_the_same_moment(db):
    shelf = Category.objects.create(name="Sparklers")
    moment = timezone.now()
    for i in range(7):
        p = Product.objects.create(name=f"Sparkler {i}", category=shelf)
        Variant.objects.create(product=p, price="10", stock=5)
    Product.objects.update(created_at=moment)
    client, seen = APIClient(), []
    for page in (1, 2, 3):
        seen += [p["name"] for p in client.get(f"/api/v1/products/?page={page}&page_size=3").json()["results"]]
    assert seen == [f"Sparkler {i}" for i in range(7)]
