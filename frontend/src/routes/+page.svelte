<script>
</script>

<main class="home">

  <section class="panel ipc">
    <div class="top">
      <h1>IPC Crime Analysis</h1>
      <p>Explore crime statistics across Indian states and districts.</p>
    </div>

    <div class="features">
      <div class="card">📍 State Crime Overview</div>
      <div class="card">📈 Crime Trend Analysis</div>
      <div class="card">🏆 Top States Rankings</div>
      <div class="card">🗾 District wise Rankings</div>
    </div>

    <a href="/ipc" class="enter">Enter IPC Section</a>
  </section>


  <section class="panel cyber">
    <div class="top">
      <h1>Cyber Crime Analysis</h1>
      <p>Analyze cyber attacks, industries, and security trends across world.</p>
    </div>

    <div class="features">
      <div class="card">💻 Cyber Attack Trends</div>
      <div class="card">🏭 Industry & Target Analysis</div>
      <div class="card">📊 Data Loss & Severity </div>
      <div class="card">🛡 Mitigation & Outcome </div>
    </div>

    <a href="/cyber" class="enter">Enter Cyber Section</a>
  </section>

</main>


<style>
 main.home {
  min-height: calc(100vh - 65px);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 35px;
  padding: 45px 25px 25px 25px;
  box-sizing: border-box;
  background: linear-gradient(135deg, #fafafa, #eef5f1);
}

.panel {
  margin-top: 60px;
  width: 42%;
  min-height: 50vh;
  padding: 28px;
  border-radius: 22px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  backdrop-filter: blur(12px);
  transition: all 0.35s ease;
}

.panel:hover {
  transform: translateY(-6px);
}

.ipc {
  background: linear-gradient(135deg, #fff2e6, #fff7f0);
  box-shadow: 0 18px 45px rgba(255,140,60,0.18);
}

.cyber {
  background: linear-gradient(135deg, #e9fff4, #f4fff8);
  box-shadow: 0 18px 45px rgba(20,180,120,0.18);
}

.top h1 {
  font-size: 26px;
  margin-bottom: 4px;
  color: #1c1c1c;
  display: flex;
  align-items: center;
  justify-content: center;
}

.top p {
  color: #5c5c5c;
  font-size: 14px;
}

.features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.card {
  background: rgba(255,255,255,0.92);
  padding: 20px;
  border-radius: 14px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.05);
  font-weight: 500;
  font-size: 14px;
  color: #2c2c2c;
  animation: float 4s ease-in-out infinite;
  transition: all 0.25s ease;
}

.ipc .card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 28px rgba(255,140,60,0.30);
}

.cyber .card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 28px rgba(19,183,137,0.30);
}

.card:nth-child(2){ animation-delay: 0.4s }
.card:nth-child(3){ animation-delay: 0.8s }
.card:nth-child(4){ animation-delay: 1.2s }

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
  100% { transform: translateY(0px); }
}

.enter {
  margin-top: 6px;
  width: fit-content;
  padding: 11px 22px;
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.25s ease;
}

.ipc .enter {
  background: linear-gradient(135deg, #ff8c3c, #fb7324);
}

.ipc .enter:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 30px rgba(255,140,60,0.35);
}

.cyber .enter {
  background: linear-gradient(135deg, #13b789, #0fa372);
}

.cyber .enter:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 30px rgba(19,183,137,0.35);
}
</style>
