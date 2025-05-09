/**
 * Generic type for API responses.
 */
export type ApiResponse<T> = {
    data: T;
    error: false;
} | {
    data: null;
    error: true;
}


/**
 * Type for the product autocomplete API response.
 */
export interface ProductAutocomplete {
    id: number;
    manufacturer: string;
    manufacturer_id: string;
    name: string;
}


/**
 * Type for the product data.
 */
export interface Product {
    id: number;
    manufacturer_id: string;
    name: string;
    manufacturer: string;
    category: string;
    base_image_url: string;
    description: string;
    piece_count: number;
    minifigures: number;
    release_year: number;
    created_at: string;
}