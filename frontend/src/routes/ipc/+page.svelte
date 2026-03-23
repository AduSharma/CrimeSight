<script>
import { onMount, tick } from "svelte";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
Chart.register(ChartDataLabels);

let states = [];
let years = [];
let crimes = [];
let districts = [];

let selectedState = "";
let selectedYear = "";
let selectedCrime = "";
let selectedDistrict = "";
let selectedN = 5;


let stateSummary = [];
let trendData = [];
let topStatesData = [];
let districtRankingData = [];


let summaryCanvas;
let trendCanvas;
let topStatesCanvas;
let districtRankingCanvas;


let summaryChart = null;
let trendChart = null;
let topStatesChart = null;
let districtRankingChart = null;

let stateSelect1;
let yearSelect;
let stateSelect2;
let crimeSelect;
let districtSelect;
let rankingYearSelect;
let rankingCrimeSelect;
let districtRankingStateSelect;
let districtRankingYearSelect;
let districtRankingCrimeSelect;

let summaryColor = "#3498db";
let trendColor = "#13b789";
let rankingColor = "#9b59b6";
let districtRankingColor = "#ff7f50";


let summaryChartType = "bar";
let trendChartType = "line";
let rankingChartType = "bar";
let districtRankingChartType = "bar";

let summaryColorSelect;
let summaryTypeSelect;
let trendColorSelect;
let trendTypeSelect;
let rankingColorSelect;
let rankingTypeSelect;
let districtRankingColorSelect;
let districtRankingTypeSelect;

function autoResizeSelect(el) {
  if (!el) return;
  const text = el.options[el.selectedIndex]?.text || "Select";
  el.style.width = (text.length * 9 + 50) + "px";
}

function resizeAll() {
  autoResizeSelect(stateSelect1);
  autoResizeSelect(yearSelect);
  autoResizeSelect(stateSelect2);
  autoResizeSelect(crimeSelect);
  autoResizeSelect(districtSelect);
  autoResizeSelect(summaryColorSelect);
  autoResizeSelect(summaryTypeSelect);
  autoResizeSelect(trendColorSelect);
  autoResizeSelect(trendTypeSelect);
  autoResizeSelect(rankingColorSelect);
  autoResizeSelect(rankingTypeSelect);
  autoResizeSelect(rankingYearSelect);
  autoResizeSelect(rankingCrimeSelect);
  autoResizeSelect(districtRankingStateSelect);
  autoResizeSelect(districtRankingYearSelect);
  autoResizeSelect(districtRankingCrimeSelect);
  autoResizeSelect(districtRankingColorSelect);
  autoResizeSelect(districtRankingTypeSelect);
}

function saveLocal() {
  sessionStorage.setItem("ipcState", JSON.stringify({
    selectedState,
    selectedYear,
    selectedCrime,
    selectedDistrict,
    stateSummary,
    trendData,
    selectedN,
    topStatesData,
    districtRankingData
  }));
}

function loadLocal() {
  const saved = sessionStorage.getItem("ipcState");
  if (!saved) return;
  const d = JSON.parse(saved);
  selectedState = d.selectedState || "";
  selectedYear = d.selectedYear || "";
  selectedCrime = d.selectedCrime || "";
  selectedDistrict = d.selectedDistrict || "";
  stateSummary = d.stateSummary || [];
  trendData = d.trendData || [];
  topStatesData = d.topStatesData || [];
  selectedN = d.selectedN || "";
  districtRankingData = d.districtRankingData || [];

}

async function loadDropdowns() {
  states = (await (await fetch("http://localhost:8000/ipc/states")).json()).states;
  years = (await (await fetch("http://localhost:8000/ipc/years")).json()).years;
  crimes = (await (await fetch("http://localhost:8000/ipc/crimes")).json()).crimes;
}

async function loadDistricts() {
  if (!selectedState) return;
  const safeState = encodeURIComponent(selectedState);
  const res = await fetch(`http://localhost:8000/ipc/districts?state=${safeState}`);
  districts = (await res.json()).districts || [];
  await tick();
  resizeAll();
}

async function loadStateSummary() {
  if (!selectedState || !selectedYear) return;
  const safeState = encodeURIComponent(selectedState);
  const res = await fetch(`http://localhost:8000/ipc/state-summary?state=${safeState}&year=${selectedYear}`);
  const data = await res.json();
  stateSummary = data.data || [];
  await tick();
  drawSummaryChart();
  saveLocal();
}

function drawSummaryChart() {
if (!summaryCanvas || stateSummary.length === 0) return;
if (summaryChart) summaryChart.destroy();

let totalRow = stateSummary.find(r => r.DISTRICT === "TOTAL") || stateSummary[0];
let keys = Object.keys(totalRow).filter(k => !["STATE/UT","DISTRICT","YEAR"].includes(k));
let values = keys.map(k => totalRow[k]);

let type = summaryChartType === "horizontal" ? "bar" : summaryChartType;

summaryChart = new Chart(summaryCanvas, {
type,
data: {
labels: keys,
datasets: [{
label: "Crime Distribution",
data: values,
backgroundColor: summaryChartType === "pie" ? pieColors : summaryColor
}]
},
options: {
responsive: true,
maintainAspectRatio: false,
indexAxis: summaryChartType === "horizontal" ? "y" : "x",
plugins: {
legend: { display: true },
title: {
display: true,
text: selectedState + " Crime Distribution in " + selectedYear
},
datalabels: summaryChartType === "pie" ? {
color: "#fff",
font: { weight: "bold" },
formatter: (v, ctx) => {
const arr = ctx.chart.data.datasets[0].data;
const total = arr.reduce((a,b)=>a+b,0);
return ((v/total)*100).toFixed(1) + "% (" + v + ")";
}
} : false
}
}
});
}

async function loadCrimeTrend() {
  if (!selectedState || !selectedCrime) return;

  const safeState = encodeURIComponent(selectedState);
  const safeCrime = encodeURIComponent(selectedCrime);
  const safeDistrict = encodeURIComponent(selectedDistrict);

  let url = `http://localhost:8000/ipc/crime-trend?state=${safeState}&crime=${safeCrime}`;
  if (selectedDistrict) url += `&district=${safeDistrict}`;

  const res = await fetch(url);
  const data = await res.json();

  trendData = data.trend || [];

  await tick();
  drawTrendChart();
  saveLocal();
}

function drawTrendChart() {
if (!trendCanvas || trendData.length === 0) return;
if (trendChart) trendChart.destroy();

let type = trendChartType === "horizontal" ? "bar" : trendChartType;

trendChart = new Chart(trendCanvas, {
type,
data: {
labels: trendData.map(d => d.year),
datasets: [{
label: selectedCrime + " Trend",
data: trendData.map(d => d.value),
borderColor: trendColor,
backgroundColor: trendColor
}]
},
options: {
responsive: true,
maintainAspectRatio: false,
indexAxis: trendChartType === "horizontal" ? "y" : "x",
plugins: {
legend: { display: true },
title: {
display: true,
text: selectedCrime + " Trend in " + selectedState + (selectedDistrict ? " in " + selectedDistrict + " district" : " over all districts")
},
datalabels: trendChartType === "pie" ? {
color: "#fff",
font: { weight: "bold" },
formatter: (v, ctx) => {
const arr = ctx.chart.data.datasets[0].data;
const total = arr.reduce((a,b)=>a+b,0);
return ((v/total)*100).toFixed(1) + "% (" + v + ")";
}
} : false
}
}
});
}

async function loadTopStates() {
  if (!selectedCrime || !selectedYear) return;

  const safeCrime = encodeURIComponent(selectedCrime);
  let url = `http://localhost:8000/ipc/top-states?crime=${safeCrime}&year=${selectedYear}`;
  if (selectedN) url += `&n=${selectedN}`;

  const res = await fetch(url);
  const data = await res.json();
  topStatesData = data.top_states || [];

  await tick();
  drawTopStatesChart();
  saveLocal();
}

function drawTopStatesChart() {
if (!topStatesCanvas || topStatesData.length === 0) return;
if (topStatesChart) topStatesChart.destroy();

let type = rankingChartType === "horizontal" ? "bar" : rankingChartType;

topStatesChart = new Chart(topStatesCanvas, {
type,
data: {
labels: topStatesData.map(d => d.state),
datasets: [{
label: selectedCrime + " Top States",
data: topStatesData.map(d => d.value),
backgroundColor: rankingChartType === "pie" ? pieColors : rankingColor
}]
},
options: {
responsive: true,
maintainAspectRatio: false,
indexAxis: rankingChartType === "horizontal" ? "y" : "x",
plugins: {
legend: { display: true },
title: {
display: true,
text: "Top " + selectedN + " States for " + selectedCrime + " in " + selectedYear
},
datalabels: rankingChartType === "pie" ? {
color: "#fff",
font: { weight: "bold" },
formatter: (v, ctx) => {
const arr = ctx.chart.data.datasets[0].data;
const total = arr.reduce((a,b)=>a+b,0);
return ((v/total)*100).toFixed(1) + "% (" + v + ")";
}
} : false
}
}
});
}
async function loadDistrictRanking() {
  if (!selectedState || !selectedCrime || !selectedYear) return;

  const safeState = encodeURIComponent(selectedState);
  const safeCrime = encodeURIComponent(selectedCrime);

  const url = `http://localhost:8000/ipc/district-ranking?state=${safeState}&crime=${safeCrime}&year=${selectedYear}`;

  const res = await fetch(url);
  const data = await res.json();

  districtRankingData = data.districts || [];

  await tick();
  drawDistrictRankingChart();
  saveLocal();
}

function drawDistrictRankingChart() {
if (!districtRankingCanvas || districtRankingData.length === 0) return;
if (districtRankingChart) districtRankingChart.destroy();

let type = districtRankingChartType === "horizontal" ? "bar" : districtRankingChartType;

districtRankingChart = new Chart(districtRankingCanvas, {
type,
data: {
labels: districtRankingData.map(d => d.district),
datasets: [{
label: selectedCrime + " District Ranking",
data: districtRankingData.map(d => d.value),
backgroundColor: districtRankingChartType === "pie" ? pieColors : districtRankingColor
}]
},
options: {
responsive: true,
maintainAspectRatio: false,
indexAxis: districtRankingChartType === "horizontal" ? "y" : "x",
plugins: {
legend: { display: true },
title: {
display: true,
text: selectedCrime + " Ranking in districts of " + selectedState + " in " + selectedYear
},
datalabels: districtRankingChartType === "pie" ? {
color: "#fff",
font: { weight: "bold" },
formatter: (v, ctx) => {
const arr = ctx.chart.data.datasets[0].data;
const total = arr.reduce((a,b)=>a+b,0);
return ((v/total)*100).toFixed(1) + "% (" + v + ")";
}
} : false
}
}
});
}

function exportSummaryPNG() {
  if (!summaryChart) return;

  const url = summaryChart.toBase64Image();
  const safeState = selectedState ? selectedState.replace(/\s+/g, "_") : "State";
  const safeYear = selectedYear ? selectedYear : "AllYears";
  const filename = `State Crime Overview_${safeState}_${safeYear}.png`;

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
}

function exportTrendPNG() {
  if (!trendChart) return;

  const url = trendChart.toBase64Image();
  const safeState = selectedState ? selectedState.replace(/\s+/g, "_") : "State";
  const safeCrime = selectedCrime ? selectedCrime.replace(/\s+/g, "_") : "Crime";
  const safeDistrict = selectedDistrict ? selectedDistrict.replace(/\s+/g, "_") : "";

  let filename = `Crime Trend_${safeState}_${safeCrime}`;
  if (safeDistrict) filename += `_${safeDistrict}`;
  filename += ".png";

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
}

function exportTopStatesPNG() {
  if (!topStatesChart) return;

  const url = topStatesChart.toBase64Image();
  const safeCrime = selectedCrime ? selectedCrime.replace(/\s+/g, "_") : "Crime";
  const safeYear = selectedYear || "Year";
  const safeN = selectedN;

  const filename = `Top_${safeN}_States_${safeCrime}_${safeYear}.png`;

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
}

function exportDistrictRankingPNG() {
  if (!districtRankingChart) return;

  const url = districtRankingChart.toBase64Image();
  const safeState = selectedState ? selectedState.replace(/\s+/g, "_") : "State";
  const safeCrime = selectedCrime ? selectedCrime.replace(/\s+/g, "_") : "Crime";
  const safeYear = selectedYear || "Year";

  const filename = `District_Ranking_${safeState}_${safeCrime}_${safeYear}.png`;

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
}

function clearAllSelections() {
  selectedState = "";
  selectedYear = "";
  selectedCrime = "";
  selectedDistrict = "";
  districts = [];
}

function clearSummary() {
  clearAllSelections();
  stateSummary = [];
  if (summaryChart) summaryChart.destroy();
  summaryChart = null;
  sessionStorage.clear();
  tick().then(resizeAll);
}

function clearTrend() {
  clearAllSelections();
  trendData = [];
  if (trendChart) trendChart.destroy();
  trendChart = null;
  sessionStorage.clear();
  tick().then(resizeAll);
}

function clearTopStates() {
  clearAllSelections();
  selectedN = 5;
  topStatesData = [];
  if (topStatesChart) topStatesChart.destroy();
  topStatesChart = null;
  sessionStorage.clear();
  tick().then(resizeAll);
}
function clearDistrictRanking() {
  clearAllSelections();
  districtRankingData = [];
  if (districtRankingChart) districtRankingChart.destroy();
  districtRankingChart = null;
  sessionStorage.clear();
  tick().then(resizeAll);
}

onMount(async () => {
  loadLocal();
  await loadDropdowns();
  if (selectedState) loadDistricts();

  await tick();
  resizeAll();
  drawSummaryChart();
  drawTrendChart();
  drawTopStatesChart();
  drawDistrictRankingChart();
});
</script>

<main class="ipc">

<section class="block">
  <div class="header">
    <h2>State Crimes Overview</h2>

    <div class="right-controls">
      <select bind:this={stateSelect1} bind:value={selectedState} on:change={(e)=>{autoResizeSelect(e.target)}}>
        <option value="">Select State / UT</option>
        {#each states as s}<option>{s}</option>{/each}
      </select>

      <select bind:this={yearSelect} bind:value={selectedYear} on:change={(e)=>autoResizeSelect(e.target)}>
        <option value="">Select Year</option>
        {#each years as y}<option>{y}</option>{/each}
      </select>

      {#if stateSummary.length > 0}
      <select bind:this={summaryColorSelect} bind:value={summaryColor} on:change={(e)=>{autoResizeSelect(e.target); drawSummaryChart();}}>
        <option value="#3498db">Blue</option>
        <option value="#13b789">Green</option>
        <option value="#e74c3c">Red</option>
        <option value="#9b59b6">Purple</option>
        <option value="#f1c40f">Yellow</option>
      </select>

      <select bind:this={summaryTypeSelect} bind:value={summaryChartType} on:change={(e)=>{autoResizeSelect(e.target); drawSummaryChart();}}>
        <option value="bar">Bar</option>
        <option value="horizontal">Horizontal Bar</option>
      </select>
      {/if}

      <button on:click={loadStateSummary}>Load</button>
      <button on:click={exportSummaryPNG}>Export</button>
      <button class="clear" on:click={clearSummary}>Clear</button>
    </div>
  </div>

  {#if stateSummary.length > 0}
  <div class="chart-box fade">
    <canvas bind:this={summaryCanvas}></canvas>
  </div>
  {/if}
</section>

<section class="block">
  <div class="header">
    <h2>Crime Trend Analysis </h2>

    <div class="right-controls">
      <select bind:this={stateSelect2} bind:value={selectedState} on:change={(e)=>{autoResizeSelect(e.target); loadDistricts();}}>
        <option value="">Select State / UT</option>
        {#each states as s}<option>{s}</option>{/each}
      </select>

      <select bind:this={crimeSelect} bind:value={selectedCrime} on:change={(e)=>autoResizeSelect(e.target)}>
        <option value="">Select Crime</option>
        {#each crimes as c}<option>{c}</option>{/each}
      </select>

      <select bind:this={districtSelect} bind:value={selectedDistrict} on:change={(e)=>autoResizeSelect(e.target)}>
        <option value="">All Districts</option>
        {#each districts as d}<option>{d}</option>{/each}
      </select>

      {#if trendData.length > 0}
      <select bind:this={trendColorSelect} bind:value={trendColor} on:change={(e)=>{autoResizeSelect(e.target); drawTrendChart();}}>
        <option value="#13b789">Green</option>
        <option value="#e74c3c">Red</option>
        <option value="#3498db">Blue</option>
        <option value="#9b59b6">Purple</option>
        <option value="#f1c40f">Yellow</option>
      </select>

      <select bind:this={trendTypeSelect} bind:value={trendChartType} on:change={(e)=>{autoResizeSelect(e.target); drawTrendChart();}}>
        <option value="line">Line</option>
        <option value="bar">Bar</option>
      </select>
      {/if}

      <button on:click={loadCrimeTrend}>Load</button>
      <button on:click={exportTrendPNG}>Export</button>
      <button class="clear" on:click={clearTrend}>Clear</button>
    </div>
  </div>

  {#if trendData.length > 0}
  <div class="chart-box fade">
    <canvas bind:this={trendCanvas}></canvas>
  </div>
  {/if}
</section>

<section class="block">
  <div class="header">
    <h2>Top States Ranking</h2>

    <div class="right-controls">
      <select bind:this={rankingCrimeSelect} bind:value={selectedCrime} on:change={(e)=>autoResizeSelect(e.target)}>
        <option value="">Select Crime</option>
        {#each crimes as c}<option>{c}</option>{/each}
      </select>

      <select bind:this={rankingYearSelect} bind:value={selectedYear} on:change={(e)=>autoResizeSelect(e.target)}>
        <option value="">Select Year</option>
        {#each years as y}<option>{y}</option>{/each}
      </select>

      <input class="N" type="number" min="1" max = "30" bind:value={selectedN} on:input={loadTopStates} on:change={(e)=>{autoResizeSelect(e.target); drawTopStatesChart();}}/>
      {#if topStatesData.length > 0}
      <select bind:this={rankingColorSelect} bind:value={rankingColor} on:change={(e)=>{autoResizeSelect(e.target); drawTopStatesChart();}}>
        <option value="#9b59b6">Purple</option>
        <option value="#13b789">Green</option>
        <option value="#3498db">Blue</option>
        <option value="#e74c3c">Red</option>
      </select>

      <select bind:this={rankingTypeSelect} bind:value={rankingChartType} on:change={(e)=>{autoResizeSelect(e.target); drawTopStatesChart();}}>
        <option value="bar">Bar</option>
        <option value="horizontal">Horizontal Bar</option>
      </select>
      {/if}

      <button on:click={loadTopStates}>Load</button>
      <button on:click={exportTopStatesPNG}>Export</button>
      <button class="clear" on:click={clearTopStates}>Clear</button>
    </div>
  </div>

  {#if topStatesData.length > 0}
  <div class="chart-box fade">
    <canvas bind:this={topStatesCanvas}></canvas>
  </div>
  {/if}
</section>

<section class="block">
  <div class="header">
    <h2>Districts Ranking</h2>

    <div class="right-controls">
      <select bind:this={districtRankingStateSelect} bind:value={selectedState} on:change={(e)=>{autoResizeSelect(e.target)}}>
        <option value="">Select State / UT</option>
        {#each states as s}<option>{s}</option>{/each}
      </select>

      <select bind:this={districtRankingCrimeSelect} bind:value={selectedCrime} on:change={(e)=>autoResizeSelect(e.target)}>
        <option value="">Select Crime</option>
        {#each crimes as c}<option>{c}</option>{/each}
      </select>

      <select bind:this={districtRankingYearSelect} bind:value={selectedYear} on:change={(e)=>autoResizeSelect(e.target)}>
        <option value="">Select Year</option>
        {#each years as y}<option>{y}</option>{/each}
      </select>

      {#if districtRankingData.length > 0}
      <select bind:this={districtRankingColorSelect} bind:value={districtRankingColor} on:change={(e)=>{autoResizeSelect(e.target); drawDistrictRankingChart();}}>
        <option value="#ff7f50">Coral</option>
        <option value="#13b789">Green</option>
        <option value="#3498db">Blue</option>
        <option value="#9b59b6">Purple</option>
        <option value="#e74c3c">Red</option>
      </select>

      <select bind:this={districtRankingTypeSelect} bind:value={districtRankingChartType} on:change={(e)=>{autoResizeSelect(e.target); drawDistrictRankingChart();}}>
        <option value="bar">Bar</option>
        <option value="horizontal">Horizontal Bar</option>
      </select>
      {/if}

      <button on:click={loadDistrictRanking}>Load</button>
      <button on:click={exportDistrictRankingPNG}>Export</button>
      <button class="clear" on:click={clearDistrictRanking}>Clear</button>
    </div>
  </div>

  {#if districtRankingData.length > 0}
  <div class="chart-box fade">
    <canvas bind:this={districtRankingCanvas}></canvas>
  </div>
  {/if}
</section>

</main>

<style>
main.ipc { padding:25px }

.block {
  background:white;
  padding:20px;
  border-radius:14px;
  margin-top:60px;
  transition: all .3s ease;
}

.block:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0,0,0,.08);
}

.header {
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.right-controls {
  display:flex;
  gap:10px;
  flex-wrap:wrap;
}

select {
  padding:8px 14px;
  border-radius:10px;
  border:1px solid #ddd;
  transition:.2s;
  width:auto;
  min-width:100px;
  max-width:380px;
}

button {
  background:#13b789;
  color:white;
  border:none;
  padding:8px 14px;
  border-radius:10px;
}

button:hover {
  transform: scale(1.05);
}

button.clear {
  background:#e74c3c;
}
.N {
  width:34px;
  padding:8px 10px;
  border:1px solid #ddd;
  border-radius:10px;
}
.chart-box {
  height:400px;
  margin-top:25px;
}

.fade {
  animation: fadeIn 1s ease;
}

@keyframes fadeIn {
  from { opacity:0; transform: translateY(10px); }
  to { opacity:1; transform: translateY(0); }
}
</style>
