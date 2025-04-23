// import type { ApiResponse, ProductAutocomplete } from "$lib/types";


// export async function load() {
//     try {
//         const response = await fetch("http://localhost:8000/products/autocomplete");
//         const data: ProductAutocomplete[] = await response.json();
//         return {
//             autocompleteProducts: {
//                 data: data,
//                 error: false
//             } as ApiResponse<ProductAutocomplete[]>
//         }
//     } catch (error) {
//         console.error('Error in load function:', error);
//         return {
//             autocompleteProducts: {
//                 data: null,
//                 error: true
//             } as ApiResponse<ProductAutocomplete[]>
//         }
//     }
// }
