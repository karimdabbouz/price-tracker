<script lang="ts">
    import "../../../index.css";
    import Navbar from "../../../components/Navbar.svelte";
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { manufacturers } from "$lib/stores";
    import { API_URL } from "$lib/config";

    // state
    let manufacturer: string | undefined;
    let products: any[] = []; // add proper type later
    let state = {
        limit: 1,
        offset: 0,
        release_year: [2025, 2024],
        loading: false,
        total_count: 0
    }

    // load function
    const loadProducts = async () => {
        state.loading = true;
        const filterParams = new URLSearchParams();
        Object.entries(state).forEach(([key, value]) => {
            if (key === 'release_year' && Array.isArray(value) && value.length > 0) {
                value.forEach((v) => filterParams.append(key, String(v)));
            } else if (key !== 'release_year') {
                filterParams.append(key, String(value));
            }
        });
        console.log(filterParams.toString());
        const response = await fetch(
            `${API_URL}/manufacturers/${$page.params.manufacturer}/product_listings?${filterParams}`
        );
        const newProducts = await response.json();
        state.total_count = newProducts[1];
        state.loading = false;
        if (state.offset === 0) {
            products = newProducts[0];
        } else {
            products = [...products, ...newProducts[0]];
        }
    }

    // load more function
    const loadMore = async () => {
        state.offset += state.limit;
        await loadProducts();
    }

    // set manufacturer name from url param
    onMount(() => {
        manufacturer = $manufacturers.find(m => m.toLowerCase() === $page.params.manufacturer.toLowerCase());
    });

    // load products from api
    onMount(async () => {
        loadProducts();
    });
</script>

<Navbar />


<div class="flex flex-col min-h-screen mx-20">

    <div class="h-60">
        <!-- Spacing -->
    </div>

    <div class="flex items-center justify-start mb-10">
        {#if manufacturer}
            <h1 class="text-8xl font-bold" style="color: #0000ff;">
                {manufacturer}
            </h1>
        {:else}
            <h1 class="text-8xl font-bold" style="color: #0000ff;">
                <!-- placeholder with same height as the other h1 -->
            </h1>
        {/if}
    </div>

    <div class="flex items-center justify-between my-4">
        <div class="flex bg-blue-500">
            <div>
                Sortieren nach: Veröffentlichungsjahr, Preis
            </div>
            <div>
                Sort direction arrow
            </div>
            <div>
                Checkbox: Angebote mit mehreren Preisen zuerst anzeigen
            </div>
        </div>
        <div class="bg-red-500">
            ende
        </div>
    </div>

    <div class="flex-1 my-4">
        <div class="grid grid-cols-5 gap-4">
            {#if products.length > 0}
                {#each products as item}
                    <div class="h-88 p-4 flex flex-col" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
                    <h2 class="text-l">{item.name}</h2>
                    <div class="flex flex-grow">
                        <img src="/images/logos/cada.webp" alt="test" class="w-full object-contain">
                    </div>
                    <div class="flex gap-2 mt-auto">
                        <p>{item.prices.length} Preis(e)</p>
                        <p>
                            {item.prices.length > 0
                                ? Math.min(...item.prices.map(p => p.price))
                                    .toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '€'
                                : '–'}
                        </p>
                    </div>
                    </div>
                {/each}
                {#if state.total_count > products.length}
                    <div class="h-88 p-4 flex flex-col" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
                        <button on:click={loadMore} disabled={state.loading}>
                            {state.loading ? 'Loading...' : 'Load More'}
                        </button>
                    </div>
                {/if}
            {:else}
                <p>loading...</p> <!-- TODO: should not display loading when no products are found -->
            {/if}
        </div>
    </div>

</div>