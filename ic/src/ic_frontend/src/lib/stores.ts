import { writable } from "svelte/store";
import type { ProductAutocomplete } from "./types";


export const autocompleteProducts = writable<ProductAutocomplete[]>([]);