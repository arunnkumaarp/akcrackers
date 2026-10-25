import csv
import shutil
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Category, Product, ProductImage, Variant
from orders.models import Courier

DATA = Path(settings.BASE_DIR) / "data"
UNITS = {"PKT": "1 Packet", "BOX": "1 Box"}
# Regular parcel couriers don't carry fireworks; the shop types its transport company when it ships.
NO_FIREWORKS = ["DHL", "The Professional Couriers"]


def slug(name):
    return "".join(ch if ch.isalnum() else "-" for ch in name.lower()).strip("-").replace("--", "-")


class Command(BaseCommand):
    help = (
        "Load the crackers price list: one shelf per category in the list's order, one product per row, "
        "sold at the offer price with the MRP shown. Running it again updates prices without touching stock."
    )

    def add_arguments(self, parser):
        parser.add_argument("csv", nargs="?", default=str(DATA / "price_list_2026.csv"),
                            help="code,name,category,unit,mrp,offer_price (default: data/price_list_2026.csv)")
        parser.add_argument("--stock", type=int, default=50, help="Stock for new products (default 50)")
        parser.add_argument("--replace", action="store_true",
                            help="Delete every existing product and shelf first, for a clean catalog")

    @transaction.atomic
    def handle(self, *args, **options):
        path, stock, replace = Path(options["csv"]), options["stock"], options["replace"]
        if not path.exists():
            raise CommandError(f"No price list at {path}")
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        if replace:
            # Past orders keep their own copy of names and prices, so removing products doesn't change them.
            Product.objects.all().delete()
            Category.objects.all().delete()

        shelves, made, updated = {}, 0, 0
        for row in rows:
            name = row["category"].strip()
            if name not in shelves:
                shelf = Category.objects.filter(name=name).first() or Category(name=name)
                shelf.sort_order, shelf.is_active = len(shelves), True
                shelf.save()
                shelves[name] = shelf
            shelf = shelves[name]

            code = int(row["code"])
            unit = UNITS.get(row["unit"].strip().upper(), row["unit"].strip())
            mrp, price = Decimal(row["mrp"]), Decimal(row["offer_price"])
            sku = f"AK-{code:03d}"
            off = round((1 - price / mrp) * 100) if mrp else 0
            description = f"Code {code} · {unit.replace('1 ', 'per ').lower()} · {off}% off MRP"

            variant = Variant.objects.select_related("product").filter(sku=sku).first()
            if variant:
                product = variant.product
                product.name, product.category, product.description = row["name"].strip(), shelf, description
                product.save()
                variant.size, variant.price, variant.mrp = unit, price, mrp
                variant.save()
                updated += 1
            else:
                product = Product.objects.create(name=row["name"].strip(), category=shelf, description=description)
                Variant.objects.create(product=product, sku=sku, size=unit, price=price, mrp=mrp, stock=stock)
                made += 1

            art = self.art_for(name)
            if art and not product.images.exists():
                ProductImage.objects.create(product=product, alt=name, image=art)

        Courier.objects.filter(name__in=NO_FIREWORKS).update(is_active=False)
        self.stdout.write(self.style.SUCCESS(
            f"{len(shelves)} shelves, {made} products added, {updated} updated (new products start with {stock} in stock)."))

    def art_for(self, category):
        """The shelf's picture, copied into media once and shared by its products until the shop uploads photos."""
        source = DATA / "art" / f"{slug(category)}.jpg"
        if not source.exists():
            return None
        stored = f"products/art/{source.name}"
        target = Path(settings.MEDIA_ROOT) / stored
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        return stored
