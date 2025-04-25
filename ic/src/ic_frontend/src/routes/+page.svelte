<script lang="ts">
    import "../index.css";
    import Navbar from "../components/Navbar.svelte";
    import { manufacturers, newProducts } from "$lib/stores";
</script>


<Navbar />

<div class="grid grid-cols-12 grid-rows-[260px_auto_auto] min-h-screen gap-2" style="background-color: #F8FAFC;">
    <div class="col-span-12"></div>
    
    <div class="col-start-2 col-span-6">
        <h1 class="text-8xl font-bold" style="color: #0000ff;">
            Alternative<br>
            Klemmbausteine im<br>
            Preisvergleich
        </h1>
    </div>
    
    <div class="col-span-12 grid grid-cols-12 auto-rows-auto gap-2 mt-20">
        <div class="col-start-2 col-span-3 mb-4">
            <h2 class="text-3xl" style="color: #1E293B">
                Marken
            </h2>
        </div>
        <div class="col-start-5 col-span-3 mb-4">
            <h2 class="text-3xl" style="color: #1E293B">
                Neuheiten
            </h2>
        </div>
        
        <div class="col-start-2 col-span-3">
            {#each $manufacturers as manufacturer}
                    <div class="h-64 mb-2 flex items-center justify-center p-4" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
                        <a href="/marken/{manufacturer.toLowerCase()}">
                            <img src="/images/logos/{manufacturer.toLowerCase()}.webp" alt="{manufacturer}" class="w-full h-full object-contain">
                        </a>
                    </div>
            {/each}
        </div>
        
        <div class="col-start-5 col-span-3">
            {#each $newProducts as newProduct}
                <div class="h-64 mb-2 flex items-center p-4" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
                    {newProduct}
                </div>
            {/each}
        </div>
    </div>
</div>
