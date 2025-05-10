<script lang="ts">
    import "../../index.css";
    import { manufacturers } from "$lib/stores";
</script>


<div class="flex flex-col min-h-screen mx-20">

    <div class="h-40">
        <!-- Spacing -->
    </div>

    <div class="flex items-center justify-start mb-10">
        <h1 class="text-8xl font-bold" style="color: #0000ff;">
            Marken
        </h1>
    </div>

    <div class="flex items-center justify-between my-4">
        <div class="flex bg-blue-500">
            <div>
                checkbox: nach anzahl preisen sortiert
            </div>
        </div>
        <div class="bg-red-500">
            drei
        </div>
    </div>

    <div class="flex-1 my-4">
        <div class="grid grid-cols-5 gap-4">
            {#each Object.values($manufacturers) as item}
                <div class="h-64 p-4" style="background-color: #ffffff; border: 4px solid #E2E8F0;">
                    <a href="/marken/{item.toLowerCase()}">
                        <img src="/images/logos/{item.toLowerCase()}.webp" alt="{item}" class="w-full h-full object-contain">
                    </a>
                </div>
            {/each}
        </div>
    </div>

</div>