<script lang="ts">
    import "../../../index.css";
    import { manufacturers, retailersStore } from "../../../lib/stores";
    import { onMount } from "svelte";
    import { API_URL } from "../../../lib/config";
    import { Lightbox } from 'svelte-lightbox';

    export let data;

    let prices = [];

    onMount(async () => {
        const response = await fetch(`${API_URL}/products/${data.product.id}/prices`);
        prices = (await response.json()).sort((a, b) => a.price - b.price);
    });
</script>


<div class="flex flex-col min-h-screen mx-20">

    <div class="h-40">
        <!-- Spacing -->
    </div>

    <div class="flex items-center justify-start">
        <h1 class="text-8xl font-bold" style="color: #0000ff;">
            {$manufacturers[data.product.manufacturer] ?? data.product.manufacturer} - {data.product.name}
        </h1>
    </div>

    <div class="flex items-center mt-4 mb-20">
        <div class="flex">
            <h2 class="text-xl">Set-Nummer: {data.product.manufacturer_id}</h2>
        </div>
    </div>

    <div class="flex flex-row my-4 gap-x-10 min-h-[50vh]">
        <div class="flex-1 p-10 bg-white border-4 border-slate-200 flex items-center justify-center">
            <Lightbox>
                <img src="https://drp6pdts0tcog.cloudfront.net/COBI-5763-0.webp" alt="Produktbild 1" />
            </Lightbox>
        </div>
        <div class="flex-1 flex flex-col p-10 bg-white border-4 border-slate-200">
            <div class="flex flex-col h-full justify-between">
                <div>
                    <h1 class="text-4xl font-bold text-slate-900 mb-2">
                        {$manufacturers[data.product.manufacturer] ?? data.product.manufacturer} - {data.product.name}
                    </h1>
                    <div class="text-lg text-slate-600 mb-6 flex flex-col gap-1">
                        <span>Veröffentlichungsjahr: {data.product.release_year}</span>
                        <span>Teileanzahl: {data.product.piece_count}</span>
                    </div>
                </div>
                {#if prices.length > 0}
                    <div class="grid grid-cols-[1fr_auto] items-center gap-6 bg-pink-50 border-2 border-pink-500 rounded-lg p-6 shadow-lg mt-8">
                        <div>
                            <div class="text-lg text-slate-700 mb-1">Niedrigster Preis</div>
                            <div class="text-5xl font-extrabold text-pink-600 mb-2">{prices[0].price} €</div>
                        </div>
                        <a href={prices[0].url} target="_blank"
                            class="px-8 py-4 font-bold text-xl rounded-lg shadow bg-pink-600 text-white hover:bg-pink-700 transition">
                            Zum Shop
                        </a>
                    </div>
                {/if}
            </div>
        </div>
    </div>

    <div class="min-h-[50vh] p-10" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
        <h2 class="text-3xl" style="color: #1E293B">
            Preise
        </h2>

        <div class="mt-8">
            <div class="flex flex-col gap-4">
                {#each prices as price, i}
                    <div class="grid grid-cols-3 items-center p-4 rounded
                        {i === 0
                            ? 'border-2 border-pink-500 bg-pink-50'
                            : 'border border-gray-300 bg-gray-50'}">
                        <div class="flex items-center gap-4">
                            <img src={$retailersStore.find(retailer => retailer.id === price.retailer_id)?.base_image_url}
                                 alt={$retailersStore.find(retailer => retailer.id === price.retailer_id)?.name}
                                 class="w-10 h-10 object-contain" />
                            <span class="font-bold text-lg">
                                {$retailersStore.find(retailer => retailer.id === price.retailer_id)?.name}
                            </span>
                        </div>
                        <div class="flex flex-col items-center">
                            <span class="text-2xl font-bold {i === 0 ? 'text-pink-600' : 'text-gray-800'}">
                                {price.price}&nbsp;€
                            </span>
                            {#if i === 0}
                                <span class="text-xs text-green-700 font-semibold bg-green-100 px-2 py-1 rounded min-w-[120px] text-center block">
                                    Günstigster Preis
                                </span>
                            {:else}
                                <span class="text-xs text-gray-600 bg-gray-200 px-2 py-1 rounded min-w-[120px] text-center block">
                                    +{(price.price - prices[0].price).toFixed(2)}&nbsp;€
                                </span>
                            {/if}
                        </div>
                        <a href={price.url} target="_blank" class="px-4 py-2 font-semibold text-white rounded justify-self-end"
                           style="background-color: {i === 0 ? '#FF0071' : '#64748B'};">
                            Zum Shop
                        </a>
                    </div>
                {/each}
            </div>
        </div>


        <!-- <div class="mt-8">
            <div class="flex flex-col gap-4">
                <div class="flex items-center justify-between p-4 rounded border-2 border-pink-500 bg-pink-50">
                    <div class="flex items-center gap-4">
                        <img src="" alt="Amazon" class="w-10 h-10 object-contain" />
                        <span class="font-bold text-lg">Amazon</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-2xl font-bold text-pink-600">32,55&nbsp;€</span>
                        <span class="text-xs text-green-700 font-semibold bg-green-100 px-2 py-1 rounded">Günstigster Preis</span>
                    </div>
                    <a href="./" class="px-4 py-2 font-semibold text-white rounded" style="background-color: #FF0071;">
                        Zum Shop
                    </a>
                </div>
                <div class="flex items-center justify-between p-4 rounded border border-gray-300 bg-gray-50">
                    <div class="flex items-center gap-4">
                        <img src="" alt="Brickshop" class="w-10 h-10 object-contain" />
                        <span class="font-bold text-lg">Brickshop</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-2xl font-bold text-gray-800">34,00&nbsp;€</span>
                        <span class="text-xs text-gray-600 bg-gray-200 px-2 py-1 rounded">+1,45&nbsp;€</span>
                    </div>
                    <a href="./" class="px-4 py-2 font-semibold text-white rounded" style="background-color: #64748B;">
                        Zum Shop
                    </a>
                </div>
                <div class="flex items-center justify-between p-4 rounded border border-gray-300 bg-gray-50">
                    <div class="flex items-center gap-4">
                        <img src="" alt="Spielzeugwelt" class="w-10 h-10 object-contain" />
                        <span class="font-bold text-lg">Spielzeugwelt</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-2xl font-bold text-gray-800">35,20&nbsp;€</span>
                        <span class="text-xs text-gray-600 bg-gray-200 px-2 py-1 rounded">+2,65&nbsp;€</span>
                    </div>
                    <a href="./" class="px-4 py-2 font-semibold text-white rounded" style="background-color: #64748B;">
                        Zum Shop
                    </a>
                </div>
            </div>
        </div> -->


    </div>
</div>