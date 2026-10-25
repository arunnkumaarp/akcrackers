import { Routes } from '@angular/router';

import { adminOnly, buyersOnly, loggedIn, loggedOut, staffOnly } from './core/guards';
import { Admin } from './pages/admin/admin';
import { CartPage } from './pages/cart/cart-page';
import { Checkout } from './pages/checkout/checkout';
import { Account } from './pages/account/account';
import { ProductPage } from './pages/product/product-page';
import { Gallery } from './pages/gallery/gallery';
import { Login } from './pages/login/login';
import { OrderPage } from './pages/orders/order-page';
import { OrdersPage } from './pages/orders/orders-page';
import { Sales } from './pages/sales/sales';
import { Signup } from './pages/signup/signup';

export const routes: Routes = [
  // One login for buyers and the shop team; the role sends each to their own home.
  { path: '', component: Login, canActivate: [loggedOut], title: 'Log in · AK Crackers' },
  { path: 'signup', component: Signup, canActivate: [loggedOut], title: 'Create account · AK Crackers' },
  { path: 'shop', component: Gallery, canActivate: [loggedIn], title: 'Shop · AK Crackers' },
  { path: 'account', component: Account, canActivate: [loggedIn], title: 'Your account · AK Crackers' },
  { path: 'shop/:slug', component: ProductPage, canActivate: [loggedIn], title: 'Product · AK Crackers' },
  { path: 'cart', component: CartPage, canActivate: [buyersOnly], title: 'Your cart · AK Crackers' },
  { path: 'checkout', component: Checkout, canActivate: [buyersOnly], title: 'Checkout · AK Crackers' },
  { path: 'orders', component: OrdersPage, canActivate: [buyersOnly], title: 'Your orders · AK Crackers' },
  { path: 'orders/:number', component: OrderPage, canActivate: [buyersOnly], title: 'Order · AK Crackers' },
  { path: 'admin', component: Admin, canActivate: [staffOnly], title: 'Admin · AK Crackers' },
  { path: 'admin/sales', component: Sales, canActivate: [adminOnly], title: 'Sales · AK Crackers' },
  // Unknown addresses land on the shop.
  { path: '**', redirectTo: 'shop' },
];
