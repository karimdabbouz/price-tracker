<script lang="ts">
    import "../../../index.css";
    import Navbar from "../../../components/Navbar.svelte";
    import { onMount } from "svelte";
    import { page } from "$app/stores";

    onMount(() => {
        console.log(`from page.ts onmount: ${$page.params.manufacturer}`);
    });
</script>

<Navbar />


<div class="grid grid-cols-12 grid-rows-[260px_auto_auto] min-h-screen gap-2" style="background-color: #F8FAFC;">
    <div class="col-span-12"></div>
    
    <div class="col-start-2 col-span-6">
        <h1 class="text-8xl font-bold" style="color: #0000ff;">
            hi
        </h1>
    </div>

    <div class="col-span-12 grid grid-cols-12 gap-2 mt-20">
        <div class="col-start-2 col-span-10">
            <div class="grid grid-cols-5 gap-4">
                hi
                <!-- {#each $manufacturers as item}
                    <div class="h-64 p-4" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
                        <a href="/marken/{item.toLowerCase()}">
                            <img src="/images/logos/{item.toLowerCase()}.webp" alt="{item}" class="w-full h-full object-contain">
                        </a>
                    </div>
                {/each} -->
            </div>
        </div>
    </div>
</div>