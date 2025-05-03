<script lang="ts">
    import { page } from '$app/stores';
    import "../../../index.css";
    $: ({ id, manufacturer, manufacturer_id, name } = $page.params);
</script>


single product page hello

{id}
{manufacturer}
{manufacturer_id}
{name}