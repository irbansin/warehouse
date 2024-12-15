export interface Product {
  productId: string;
  name: string;
  description?: string;
  quantity: number;
  category?: string;
  location?: string;
  warehouseId: string;
  unitPrice: number;
  sku?: string;
  lastUpdated?: string;
}

export interface ProductFormData extends Omit<Product, 'productId'> {
  productId?: string;
}

export interface InventoryFilter {
  search?: string;
  category?: string;
  warehouse?: string;
}
