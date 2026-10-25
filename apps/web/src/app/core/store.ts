import { Injectable, inject, signal } from '@angular/core';
import type { Shop } from '@akcrackers/api';

import { Api } from './api';

/** The shop's own settings (name, tagline, UPI), loaded once and shared by every page. */
@Injectable({ providedIn: 'root' })
export class Store {
  private api = inject(Api).client;
  readonly shop = signal<Shop | null>(null);
  readonly loaded = signal(false);
  readonly failed = signal(false);

  private started = false;

  async load() {
    if (this.started) return;
    this.started = true;
    try {
      const { data } = await this.api.GET('/api/v1/shop/');
      this.shop.set(data ?? null);
      this.failed.set(!data);
    } catch {
      this.failed.set(true);
    }
    this.loaded.set(true);
  }
}
