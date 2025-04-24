import { writable } from "svelte/store";
import type { ProductAutocomplete } from "./types/types";


export const autocompleteProducts = writable<ProductAutocomplete[]>([]);