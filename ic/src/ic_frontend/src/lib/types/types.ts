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
    name: string;
}