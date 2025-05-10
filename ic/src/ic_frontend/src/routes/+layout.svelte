<script lang="ts">
    import Navbar from "../components/Navbar.svelte";
    import { autocompleteProducts } from "$lib/stores";
    import { onMount } from "svelte";
    import type { ProductAutocomplete } from "$lib/types/types";
    import products from "$lib/data/products.json";

    onMount(() => {
        console.log("hi from root +layout.svelte");
        const productsAutocomplete: ProductAutocomplete[] = products.map((entry) => ({
            id: entry.id,
            manufacturer: entry.manufacturer,
            manufacturer_id: entry.manufacturer_id,
            name: entry.name
        }));
        autocompleteProducts.set(productsAutocomplete);
    });
</script>

<Navbar />

<slot />