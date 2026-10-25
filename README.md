# akcrackers

AK Crackers: an online crackers shop for Diwali — sparklers, flower pots, chakkars, rockets, sky shots, gift boxes and more, at offer prices. Django REST API, Angular web app and React Native mobile app. Cash on delivery and UPI QR payments.

## What's inside

| Part | Where | What it does |
|---|---|---|
| API | `backend/` | Django REST: accounts (password login, signup), catalog, cart, checkout, orders, UPI payment checks, sales reports |
| Price list | `backend/data/` | `price_list_2026.csv` (220 products in 23 categories) and the category pictures in `art/` |
| Web app | `apps/web/` | Angular. Buyers shop, pay and track orders; the shop team runs the admin desk. Installable on phones (PWA) |
| Mobile app | `apps/mobile/` | Expo / React Native buyer app for Android and iOS |
| API client | `packages/api/` | Typed client generated from the API's OpenAPI schema, shared by web and mobile |

**Buyers:** sign up, shop by category, search and sort, product pages with MRP and offer price, cart, checkout with UPI or cash on delivery, pay by scanning the shop's QR (or open a UPI app), send the payment reference, track the parcel, cancel before packing, manage their account.

**Shop team (web admin desk):** Orders (pack → ship with the transport company and tracking number → deliver, print packing slips, cancel), Products (add, edit, hide, stock badges), Shelves, Payments (verify or reject UPI payments, set the UPI ID and QR), Shop settings, and a Sales page for admins (revenue, sales by category and product, buyers).

## Run it

```bash
cp backend/.env.example backend/.env      # then fill it in, including DJANGO_SECRET_KEY
docker compose up -d                      # Postgres on :5434, API on :8002
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py import_price_list   # load the crackers price list
docker compose exec backend python manage.py createsuperuser

cd apps/web && npm install && npm start   # web on http://localhost:4300

cd apps/mobile && npm install
npx expo start                            # scan with Expo Go, or:
npm run android                           # build and install on an emulator / phone
```

On the Android emulator, `adb reverse tcp:8002 tcp:8002` lets the app reach the API on your computer. For a real server set `EXPO_PUBLIC_API_URL`.

### Updating the price list

Edit `backend/data/price_list_2026.csv` (columns `code,name,category,unit,mrp,offer_price`) or pass another file, then run `import_price_list` again. It updates names and prices by code and leaves stock alone. New products start with `--stock 50`; `--replace` clears the old catalog first. Products without photos show their category's picture until the shop uploads its own on the admin desk.

After changing the API, regenerate the shared client: `cd packages/api && npm run build`.

## Tests

```bash
docker compose exec backend pytest        # API
cd apps/web && npm test                   # web unit tests
cd apps/web && npm run e2e                # browser tests: every buyer and admin scenario in headless Chrome
cd apps/mobile && npm run typecheck
```

The browser tests need the API and web app running. They make their own `e2e-…` accounts and `E2E …` products and delete them afterwards.

## Screenshots

### Web

| Login | Shop | Product |
|---|---|---|
| ![Login](docs/screenshots/web/01-login.png) | ![Shop](docs/screenshots/web/03-shop.png) | ![Product](docs/screenshots/web/04-product.png) |

| Cart | Checkout | On a phone |
|---|---|---|
| ![Cart](docs/screenshots/web/05-cart.png) | ![Checkout](docs/screenshots/web/06-checkout.png) | ![Shop on a phone](docs/screenshots/web/07-shop-phone.png) |

| Admin: orders | Admin: products | Admin: shelves |
|---|---|---|
| ![Admin orders](docs/screenshots/web/08-admin-orders.png) | ![Admin products](docs/screenshots/web/09-admin-products.png) | ![Admin shelves](docs/screenshots/web/10-admin-shelves.png) |

| Sales | Signup |
|---|---|
| ![Sales](docs/screenshots/web/11-admin-sales.png) | ![Signup](docs/screenshots/web/02-signup.png) |

### Mobile (Android)

| Splash | Login | Shop | Search |
|---|---|---|---|
| ![Splash](docs/screenshots/mobile/00-splash.png) | ![Login](docs/screenshots/mobile/01-login.png) | ![Shop](docs/screenshots/mobile/03-shop.png) | ![Search](docs/screenshots/mobile/02-search.png) |

| Product | Cart | Checkout | App icon |
|---|---|---|---|
| ![Product](docs/screenshots/mobile/04-product.png) | ![Cart](docs/screenshots/mobile/05-cart.png) | ![Checkout](docs/screenshots/mobile/06-checkout.png) | ![App icon](docs/screenshots/mobile/09-app-list.png) |

| Account | Orders |
|---|---|
| ![Account](docs/screenshots/mobile/07-account.png) | ![Orders](docs/screenshots/mobile/08-orders.png) |
