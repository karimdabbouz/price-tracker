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
    $: console.log(products);
    let filters = {
        limit: "32",
        sort_by: "release_year",
        order: "desc"
    }

    // load function
    const loadProducts = async () => {
        const filterParams = new URLSearchParams(filters);
        console.log(filterParams.toString());
        // const response = await fetch(`${API_URL}/manufacturers/${$page.params.manufacturer}/products?${new URLSearchParams(filters)}`);
        // products = await response.json();
    }

    loadProducts();

    // set manufacturer name from url param
    onMount(() => {
        manufacturer = $manufacturers.find(m => m.toLowerCase() === $page.params.manufacturer.toLowerCase());
    });

    // // load products from api
    // onMount(async () => {
    //     const response = await fetch(`${API_URL}/manufacturers/${$page.params.manufacturer}/products?limit=16`);
    //     products = await response.json();
    // });
</script>

<Navbar />


<div class="grid grid-cols-12 grid-rows-[260px_auto_auto] min-h-screen gap-2" style="background-color: #F8FAFC;">
    <div class="col-span-12"></div>
    
    <div class="col-start-2 col-span-6">
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

    <div class="col-span-12 grid grid-cols-12 gap-2 mt-20">
        <div class="col-start-2 col-span-10">
            <div class="grid grid-cols-5 gap-4">
                {#each products as item}
                    <div class="h-88 p-4 flex flex-col" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
                        <h2 class="text-l">{item.name}</h2>
                        <div class="flex flex-grow">
                            <img src="/images/logos/cada.webp" alt="test" class="w-full object-contain">
                        </div>
                        <div class="flex gap-2 mt-auto">
                            <p>Preis</p>
                            <p>Beschreibung</p>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>

<div class="grid min-h-screen">
    hello
</div>