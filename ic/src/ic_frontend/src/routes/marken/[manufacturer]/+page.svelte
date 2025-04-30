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
    let showReleaseYearDropdown = false;
    const currentYear = new Date().getFullYear();
    let state = {
        limit: 1,
        offset: 0,
        release_year: [currentYear, currentYear - 1],
        loading: false,
        total_count: 0
    }
    $: console.log(state);

    
    // Helper to get all years from 2020 to max in state.release_year
    $: availableYears = Array.from({ length: currentYear - 2020 + 1 }, (_, i) => 2020 + i);


    // Toggle year selection: add if not present, remove if present
    const toggleYear = (year: number) => {
        if (state.release_year.includes(year)) {
            state.release_year = state.release_year.filter(y => y !== year);
        } else {
            state.release_year = [...state.release_year, year];
            showReleaseYearDropdown = false;
        };
        state = {
            limit: 1,
            offset: 0,
            release_year: state.release_year,
            loading: false,
            total_count: 0
        };
        loadProducts();
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
        <div class="relative w-full">
            <button
                type="button"
                class="flex flex-wrap gap-2 p-2 border border-gray-300 rounded-md bg-white cursor-pointer w-full text-left"
                on:click={() => showReleaseYearDropdown = !showReleaseYearDropdown}
            >
                {#each state.release_year as year (year)}
                    <span class="flex items-center bg-blue-100 text-blue-800 px-2 py-1 rounded">
                        {year}
                        <button
                            type="button"
                            class="ml-1 text-blue-500 hover:text-blue-700 focus:outline-none"
                            on:click|stopPropagation={() => toggleYear(year)}
                            aria-label="Remove year"
                        >×</button>
                    </span>
                {/each}
                <span class="text-gray-400">{state.release_year.length === 0 ? 'Veröffentlicht in...' : ''}</span>
            </button>
            {#if showReleaseYearDropdown}
                <ul class="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-md max-h-48 overflow-auto shadow">
                    {#each availableYears as year (year)}
                        {#if !state.release_year.includes(year)}
                            <li class="px-4 py-2 hover:bg-blue-100 cursor-pointer" role="option" aria-selected="false">
                                <button
                                    type="button"
                                    class="w-full text-left"
                                    on:click={() => toggleYear(year)}
                                >
                                    {year}
                                </button>
                            </li>
                        {/if}
                    {/each}
                </ul>
            {/if}
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