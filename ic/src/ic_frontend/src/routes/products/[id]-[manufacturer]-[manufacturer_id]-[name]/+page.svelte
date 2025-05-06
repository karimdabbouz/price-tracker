<script lang="ts">
    import "../../../index.css";
    import Navbar from "../../../components/Navbar.svelte";

    export let data;
</script>

<Navbar />


<div class="flex flex-col min-h-screen mx-20">

    <div class="h-40">
        <!-- Spacing -->
    </div>

    <div class="flex items-center justify-start mb-10">
        <h1 class="text-8xl font-bold" style="color: #0000ff;">
            {data.product.manufacturer} - {data.product.name}
        </h1>
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
    </div>

</div>