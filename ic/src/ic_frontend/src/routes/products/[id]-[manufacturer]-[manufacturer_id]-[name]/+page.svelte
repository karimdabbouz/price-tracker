<script lang="ts">
    import "../../../index.css";
    import Navbar from "../../../components/Navbar.svelte";
    import { manufacturers } from "../../../lib/stores";

    export let data;
</script>

<Navbar />


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
        <div class="flex-1 p-10" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
            <img src="https://drp6pdts0tcog.cloudfront.net/COBI-5763-0.webp" alt="product" class="w-full h-full object-contain">
        </div>
        <div class="flex-1 flex flex-col p-10" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
            <div class="mt-auto flex justify-between">
                <div>
                    <h1 class="text-3xl">
                        Niedrigster Preis:
                        <span style="color: #FF0071;">32,55 €</span>
                    </h1>
                </div>
                <button class="px-6 py-4 font-bold text-xl" style="background-color: #FF0071; color: #F8FAFC;">
                    Zu Amazon
                </button>
            </div>
        </div>
    </div>

    <div class="min-h-[50vh] p-10" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
        <h2 class="text-3xl" style="color: #1E293B">
            Preise
        </h2>
        <!-- Price comparison mockup start -->
        <div class="mt-8">
            <div class="flex flex-col gap-4">
                <!-- Cheapest retailer (already highlighted above, but included for completeness) -->
                <div class="flex items-center justify-between p-4 rounded border-2 border-pink-500 bg-pink-50">
                    <div class="flex items-center gap-4">
                        <img src="/retailer-logos/amazon.png" alt="Amazon" class="w-10 h-10 object-contain" />
                        <span class="font-bold text-lg">Amazon</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-2xl font-bold text-pink-600">32,55&nbsp;€</span>
                        <span class="text-xs text-green-700 font-semibold bg-green-100 px-2 py-1 rounded">Günstigster Preis</span>
                    </div>
                    <a href="#" class="px-4 py-2 font-semibold text-white rounded" style="background-color: #FF0071;">
                        Zum Shop
                    </a>
                </div>
                <!-- Other retailers -->
                <div class="flex items-center justify-between p-4 rounded border border-gray-300 bg-gray-50">
                    <div class="flex items-center gap-4">
                        <img src="/retailer-logos/brickshop.png" alt="Brickshop" class="w-10 h-10 object-contain" />
                        <span class="font-bold text-lg">Brickshop</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-2xl font-bold text-gray-800">34,00&nbsp;€</span>
                        <span class="text-xs text-gray-600 bg-gray-200 px-2 py-1 rounded">+1,45&nbsp;€</span>
                    </div>
                    <a href="#" class="px-4 py-2 font-semibold text-white rounded" style="background-color: #64748B;">
                        Zum Shop
                    </a>
                </div>
                <div class="flex items-center justify-between p-4 rounded border border-gray-300 bg-gray-50">
                    <div class="flex items-center gap-4">
                        <img src="/retailer-logos/spielzeugwelt.png" alt="Spielzeugwelt" class="w-10 h-10 object-contain" />
                        <span class="font-bold text-lg">Spielzeugwelt</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-2xl font-bold text-gray-800">35,20&nbsp;€</span>
                        <span class="text-xs text-gray-600 bg-gray-200 px-2 py-1 rounded">+2,65&nbsp;€</span>
                    </div>
                    <a href="#" class="px-4 py-2 font-semibold text-white rounded" style="background-color: #64748B;">
                        Zum Shop
                    </a>
                </div>
            </div>
        </div>
        <!-- Price comparison mockup end -->
    </div>

</div>