<script lang="ts">
    import { autocompleteProducts } from "$lib/stores";
    import { onMount } from "svelte";
    import type { ProductAutocomplete } from "$lib/types/types";
    import { API_URL } from "$lib/config";
    import AutoComplete from "simple-svelte-autocomplete";
    // https://github.com/pstanoev/simple-svelte-autocomplete


    onMount(async () => {
        const response = await fetch(`${API_URL}/products/autocomplete`);
        const data: ProductAutocomplete[] = await response.json();
        autocompleteProducts.set(data);
    })

    let choice: string;
</script>


<nav class="grid grid-cols-2 fixed h-16 sm:h-20 w-full px-2 sm:px-4">
	<div class="flex items-center" />
	<div class="flex justify-end items-center">
		<ul class="flex items-center text-xs sm:text-sm md:text-base">
            <li class="mx-1 sm:mx-2 md:mx-4 lg:mx-10">
                <AutoComplete items="{$autocompleteProducts.map(product => `${product.manufacturer} ${product.name}`)}" bind:selectedItem="{choice}" placeholder="Set suchen..." maxItemsToShowInList=5 hideArrow={true}/>
            </li>
            <li class="mx-1 sm:mx-2 md:mx-4 lg:mx-10"><p>{choice}</p></li>
			<li class="mx-1 sm:mx-2 md:mx-4 lg:mx-10"><a href="/" class="p-1 sm:p-2">Marken</a></li>
			<li class="mx-1 sm:mx-2 md:mx-4 lg:mx-10"><a href="/" class="p-1 sm:p-2">FAQ</a></li>
		</ul>
	</div>
</nav>