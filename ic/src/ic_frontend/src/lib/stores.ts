import { writable, readable } from "svelte/store";
import type { ProductAutocomplete } from "./types/types";


export const autocompleteProducts = writable<ProductAutocomplete[]>([]);

export const manufacturers = readable(["CaDA", "Cobi", "Bluebrixx", "Lumibricks", "Pantasy"]);
export const newProducts = readable(["eins", "zwei", "drei", "vier", "fünf"]);