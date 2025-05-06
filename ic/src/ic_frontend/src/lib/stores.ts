import { writable, readable } from "svelte/store";
import type { ProductAutocomplete } from "./types/types";


export const autocompleteProducts = writable<ProductAutocomplete[]>([]);

export const manufacturers = readable({
    "cada": "CaDA",
    "cobi": "Cobi",
    "bluebrixx": "Bluebrixx",
    "lumibricks": "Lumibricks",
    "pantasy": "Pantasy"
});
export const newProducts = readable(["eins", "zwei", "drei", "vier", "fünf"]);