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
    let filters = {
        limit: "20",
        sort_by: "release_year",
        order: "desc",
        sort_by_num_prices: true
    }

    // load function
    const loadProducts = async () => {
        const filterParams = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== undefined && value !== false) {
                filterParams.append(key, String(value));
            }
        });
        console.log(filterParams.toString());
        const response = await fetch(
            `${API_URL}/manufacturers/${$page.params.manufacturer}/product_listings?${filterParams}`
        );
        products = await response.json();
        return products;
    }


    // set manufacturer name from url param
    onMount(() => {
        manufacturer = $manufacturers.find(m => m.toLowerCase() === $page.params.manufacturer.toLowerCase());
    });

    // load products from api
    onMount(async () => {
        products = await loadProducts();
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
        <div>
            eins
        </div>
        <div>
            zwei
        </div>
        <div>
            drei
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
                        <p>foo</p>
                    </div>
                    </div>
                {/each}
            {:else}
                <p>loading...</p> <!-- TODO: should not display loading when no products are found -->
            {/if}
        </div>
    </div>

</div>