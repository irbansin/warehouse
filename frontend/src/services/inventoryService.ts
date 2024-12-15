import axios from 'axios';
import { Product, ProductFormData } from '../types/inventory';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/inventory`,
});

export const inventoryService = {
  async getProducts(): Promise<Product[]> {
    const response = await api.get('/');
    return response.data;
  },

  async getProduct(id: string): Promise<Product> {
    const response = await api.get(`/${id}`);
    return response.data;
  },

  async createProduct(product: ProductFormData): Promise<Product> {
    const response = await api.post('/', product);
    return response.data;
  },

  async updateProduct(id: string, product: ProductFormData): Promise<Product> {
    const response = await api.put(`/${id}`, product);
    return response.data;
  },

  async deleteProduct(id: string): Promise<void> {
    await api.delete(`/${id}`);
  },
};
