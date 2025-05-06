import type { Product } from '$lib/types/types';
import type { PageServerLoad } from './$types';
import { API_URL } from "$lib/config";


export const load: PageServerLoad = async ({fetch, params}) => {
    const response = await fetch(`${API_URL}/products/${params.id}`);
    const product: Product = await response.json();
    return {
        product: {
            id: product.id,
            manufacturer: product.manufacturer,
            manufacturer_id: product.manufacturer_id,
            name: product.name,
            category: product.category,
            base_image_url: product.base_image_url,
            description: product.description,
            piece_count: product.piece_count,
            minifigures: product.minifigures,
            release_year: product.release_year,
            created_at: product.created_at
        }
    }
};