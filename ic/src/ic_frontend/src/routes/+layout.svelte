<script lang="ts">
    import Navbar from "../components/Navbar.svelte";
    import { autocompleteProducts, retailersStore } from "$lib/stores";
    import { onMount } from "svelte";
    import type { ProductAutocomplete } from "$lib/types/types";
    import products from "$lib/data/products.json";
    import retailers from "$lib/data/retailers.json";

    onMount(() => {
        const productsAutocomplete: ProductAutocomplete[] = products.map((entry) => ({
            id: entry.id,
            manufacturer: entry.manufacturer,
            manufacturer_id: entry.manufacturer_id,
            name: entry.name
        }));
        autocompleteProducts.set(productsAutocomplete);
        retailersStore.set(retailers);
    });
</script>

<Navbar />

<slot />