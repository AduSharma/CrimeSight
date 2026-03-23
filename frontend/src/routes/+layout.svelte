<script>
  import Navbar from "$lib/components/Navbar.svelte";
  import favicon from "$lib/assets/Favicon.png";
</script>
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<Navbar />

<main>
  <slot />
</main>

<style>
  main {
    padding-left: 20px;
    padding-right: 20px;
    background: #f5f6f8;
    min-height: 100vh;
  }
</style>
