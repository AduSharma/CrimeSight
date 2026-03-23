<script>
  import logo from "$lib/assets/logo2.png";
  import { page } from "$app/stores";
</script>

<nav class="navbar">
  <div class="left">
    <a href="/" class="logo">
      <img src={logo} alt="CrimeSight Logo" />
    </a>
  </div>

  <div class="right">
    <a href="/" class:active={$page.url.pathname === "/"}>Home</a>
    <a href="/ipc" class:active={$page.url.pathname.startsWith("/ipc")}>IPC Crimes</a>
    <a href="/cyber" class:active={$page.url.pathname.startsWith("/cyber")}>Cyber Crimes</a>
  </div>
</nav>

<style>
  .navbar {
    position: fixed;
    top: 0;
    width: 100%;
    height: 65px;
    background: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 25px;
    box-sizing: border-box;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    z-index: 1000;
  }

  .left {
    display: flex;
    align-items: center;
  }

  .logo img {
    height: 45px;
    left: 0;
  }

  .right {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .right a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 8px;
    transition: all 0.25s ease;
  }

  .right a:hover {
    background: #fd9c3b;
    color: white;
    transform: translateY(-1px);
  }

  .right a.active {
    background: #13b789;
    color: white;
    box-shadow: 0 4px 10px rgba(19,183,137,0.35);
  }

  :global(body) {
    margin: 0;
    overflow-x: hidden;
    font-family: Consolas;
  }
</style>
