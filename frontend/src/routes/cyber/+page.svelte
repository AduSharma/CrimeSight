<script>
import { onMount, tick } from "svelte";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
Chart.register(ChartDataLabels);

let attackTypes = [];
let selectedAttack = "";

let attackTrendData = [];

let attackCanvas;
let attackChart = null;

let attackColor = "#3498db";
let attackChartType = "pie";

let pieColors = [
    "#3498db",
    "#e74c3c","#13b789","#9b59b6","#f1c40f","#1abc9c","#2ecc71","#e67e22","#34495e","#d35400","#7f8c8d","#16a085","#c0392b","#8e44ad",
    "#27ae60"];

let attackSelect;
let attackTypeSelect;

let isTargetMode = false;
let isSeverityMode = false;
let isDefenseMode = false;

let years = [];
let selectedYear = "";
let hours = [];
let selectedHour = "";
let industries = [];
let selectedIndustry = "";

let industryData = [];
let targetData = [];
let dataLossData = [];
let severityData = [];
let mitigationData = [];
let outcomeData = [];

let industryCanvas;
let industryChart = null;
let industryChartType = "bar";

let targetCanvas;
let targetChart = null;
let targetChartType = "bar";

let dataLossCanvas;
let dataLossChart = null;
let dataLossChartType = "pie";

let severityCanvas;
let severityChart = null;
let severityChartType = "pie";

let mitigationCanvas;
let mitigationChart = null;
let mitigationChartType = "bar";

let outcomeCanvas;
let outcomeChart = null;
let outcomeChartType = "pie";

let yearSelect;
let attackFilterSelect;
let industryTypeSelect;
let targetTypeSelect;

let industrySelect3;
let severityYearSelect;
let severityAttackSelect;
let dataLossTypeSelect;
let severityTypeSelect;

let defenseYearSelect;
let defenseAttackSelect;
let mitigationTypeSelect;
let outcomeTypeSelect;

function autoResizeSelect(el){
 if(!el) return;
 const text = el.options[el.selectedIndex]?.text || "Select";
 el.style.width = (text.length * 9 + 50) + "px";
}

function resizeAll(){
 autoResizeSelect(attackSelect);
 autoResizeSelect(attackTypeSelect);
 autoResizeSelect(yearSelect);
 autoResizeSelect(attackFilterSelect);
 autoResizeSelect(industryTypeSelect);
 autoResizeSelect(targetTypeSelect);
autoResizeSelect(industrySelect3);
autoResizeSelect(severityYearSelect);
autoResizeSelect(severityAttackSelect);
autoResizeSelect(dataLossTypeSelect);
autoResizeSelect(severityTypeSelect);
autoResizeSelect(defenseYearSelect);
autoResizeSelect(defenseAttackSelect);
autoResizeSelect(mitigationTypeSelect);
autoResizeSelect(outcomeTypeSelect);

}

function resizeContinuously(){
 requestAnimationFrame(()=>{
  resizeAll();
  resizeContinuously();
 });
}

function saveLocal(){
 sessionStorage.setItem("cyberState", JSON.stringify({
  selectedAttack,
  attackTrendData,
  selectedYear,
  selectedHour,
  industryData,
  targetData,
  isTargetMode,
  dataLossData,
  severityData,
  isSeverityMode,
  mitigationData,
  outcomeData,
  isDefenseMode
 }));
}

function loadLocal(){
 const saved = sessionStorage.getItem("cyberState");
 if(!saved) return;
 const d = JSON.parse(saved);

 selectedAttack = d.selectedAttack || "";
 attackTrendData = d.attackTrendData || [];
 selectedYear = d.selectedYear || "";
 selectedHour = d.selectedHour || "";
 industryData = d.industryData || [];
 targetData = d.targetData || [];
 isTargetMode = d.isTargetMode || false;
 dataLossData = d.dataLossData || [];
 severityData = d.severityData || [];
 isSeverityMode = d.isSeverityMode || false;
 mitigationData = d.mitigationData || [];
 outcomeData = d.outcomeData || [];
 isDefenseMode = d.isDefenseMode || false;
}

async function loadDropdowns(){
 attackTypes = (await (await fetch("http://localhost:8000/cyber/attack-types")).json()).attack_types || [];
 years = (await (await fetch("http://localhost:8000/cyber/years")).json()).years || [];
 hours = (await (await fetch("http://localhost:8000/cyber/hours")).json()).hours || [];
 industries = (await (await fetch("http://localhost:8000/cyber/industries")).json()).industries || [];


 await tick();
 resizeAll();
}

async function loadAttackTrend(){
 if(!selectedAttack) return;

 const res = await fetch(`http://localhost:8000/cyber/attack-trend?attack=${encodeURIComponent(selectedAttack)}`);
 const data = await res.json();

 attackTrendData = data.trend || [];

 await tick();
 drawAttackChart();
 saveLocal();
}

function drawAttackChart(){
 if(!attackCanvas || attackTrendData.length === 0) return;
 if(attackChart) attackChart.destroy();

 let dataset;

 if(attackChartType === "pie"){
  dataset = {
   label: selectedAttack + " Distribution",
   data: attackTrendData.map(d=>d.count),
   backgroundColor: pieColors.slice(0,attackTrendData.length)
  };
 }else{
  dataset = {
   label: selectedAttack + " Trend",
   data: attackTrendData.map(d=>d.count),
   borderColor: attackColor,
   backgroundColor: attackColor
  };
 }

 attackChart = new Chart(attackCanvas,{
  type: attackChartType,
  data:{
   labels: attackTrendData.map(d=>d.year),
   datasets:[dataset]
  },
  options:{
   responsive:true,
   maintainAspectRatio:false,
   plugins:{
    legend:{display:true},
    title:{display:true,text:selectedAttack+" Attack Distribution"},
    datalabels: attackChartType === "pie" ? {
     color:"#fff",
     font:{weight:"bold"},
     formatter:(v,ctx)=>{
      const arr = ctx.chart.data.datasets[0].data;
      const total = arr.reduce((a,b)=>a+b,0);
      return ((v/total)*100).toFixed(1)+"% ( "+v+" )";
     }
    } : false
   }
  }
 });
}

async function loadIndustry(){
 if(!selectedYear) return;

 let url = `http://localhost:8000/cyber/industry-impact?year=${selectedYear}`;
 if(selectedAttack) url += `&attack=${encodeURIComponent(selectedAttack)}`;

 const res = await fetch(url);
 const data = await res.json();

 industryData = data.industries || [];

 await tick();
 drawIndustryChart();
 saveLocal();
}

async function loadTargets(){
 if(!selectedAttack || selectedHour === "") return;

 const res = await fetch(`http://localhost:8000/cyber/targets?attack=${encodeURIComponent(selectedAttack)}&hour=${selectedHour}`);
 const data = await res.json();

 targetData = data.targets || [];

 await tick();
 drawTargetChart();
 saveLocal();
}

function drawIndustryChart(){
 if(!industryCanvas || industryData.length === 0) return;
 if(industryChart) industryChart.destroy();

 industryChart = new Chart(industryCanvas,{
  type: industryChartType,
  data:{
   labels: industryData.map(d=>d.industry),
   datasets:[{
    label: selectedAttack +" Industry Impact",
    data: industryData.map(d=>d.count),
    backgroundColor: industryChartType === "pie" ? pieColors : "#13b789"
   }]
  },
  options:{
   responsive:true,
   maintainAspectRatio:false,
   plugins:{
    legend:{display:true},
    title:{display:true,text:( selectedAttack ? selectedAttack : "All Cyber Attacks")+ " Impact on industries in " + selectedYear},
    datalabels: industryChartType === "pie" ? {
     color:"#fff",
     formatter:(v,ctx)=>{
      const arr = ctx.chart.data.datasets[0].data;
      const total = arr.reduce((a,b)=>a+b,0);
      return ((v/total)*100).toFixed(1)+"%("+v+")";
     }
    } : false
   }
  }
 });
}

function drawTargetChart(){
 if(!targetCanvas || targetData.length === 0) return;
 if(targetChart) targetChart.destroy();

 targetChart = new Chart(targetCanvas,{
  type: targetChartType,
  data:{
   labels: targetData.map(d=>d["target system"]),
   datasets:[{
    label: "Target Systems",
    data: targetData.map(d=>d.count),
    backgroundColor: targetChartType === "pie" ? pieColors : "#9b59b6"
   }]
  },
  options:{
   responsive:true,
   maintainAspectRatio:false,
   plugins:{
    legend:{display:true},
    title:{display:true,text:selectedAttack +" Target Systems at "+selectedHour + ":00"},
    datalabels: targetChartType === "pie" ? {
     color:"#fff",
     formatter:(v,ctx)=>{
      const arr = ctx.chart.data.datasets[0].data;
      const total = arr.reduce((a,b)=>a+b,0);
      return ((v/total)*100).toFixed(1)+"%-"+v;
     }
    } : false
   }
  }
 });
}
async function loadDataLoss(){
 let url = `http://localhost:8000/cyber/data-loss`;
 if(selectedIndustry) url += `?industry=${encodeURIComponent(selectedIndustry)}`;

 const res = await fetch(url);
 const data = await res.json();

 dataLossData = data.trend || [];

 await tick();
 drawDataLossChart();
 saveLocal();
}

async function loadSeverity(){
 if(!selectedYear) return;

 let url = `http://localhost:8000/cyber/severity-summary?year=${selectedYear}`;
 if(selectedAttack) url += `&attack=${encodeURIComponent(selectedAttack)}`;

 const res = await fetch(url);
 const data = await res.json();

 severityData = data.severity_distribution || [];

 await tick();
 drawSeverityChart();
 saveLocal();
}

function drawDataLossChart(){
 if(!dataLossCanvas || dataLossData.length === 0) return;
 if(dataLossChart) dataLossChart.destroy();

 dataLossChart = new Chart(dataLossCanvas,{
  type: dataLossChartType,
  data:{
   labels: dataLossData.map(d=>d.year),
   datasets:[{
    label:"Data Loss (GB)",
    data: dataLossData.map(d=>d.data_loss_gb),
    backgroundColor: dataLossChartType === "pie" ? pieColors : "#e67e22"
   }]
  },
  options:{
   responsive:true,
   maintainAspectRatio:false,
   plugins:{
    legend:{display:true},
    title:{display:true,text:( selectedIndustry ? selectedIndustry: "All" ) +" Industries Data Loss (GB)"},
    datalabels: dataLossChartType === "pie" ? {
     color:"#fff",
     formatter:(v,ctx)=>{
      const arr = ctx.chart.data.datasets[0].data;
      const total = arr.reduce((a,b)=>a+b,0);
      return ((v/total)*100).toFixed(1)+"% - "+v+" GB";
     }
    } : false
   }
  }
 });
}

function drawSeverityChart(){
 if(!severityCanvas || severityData.length === 0) return;
 if(severityChart) severityChart.destroy();

 severityChart = new Chart(severityCanvas,{
  type: severityChartType,
  data:{
   labels: severityData.map(d=>d.severity),
   datasets:[{
    label:"Severity Distribution",
    data: severityData.map(d=>d.count),
    backgroundColor: severityChartType === "pie" ? pieColors : "#c0392b"
   }]
  },
  options:{
   responsive:true,
   maintainAspectRatio:false,
   plugins:{
    legend:{display:true},
    title:{display:true,text:" Severity-wise "+ ( selectedAttack ? selectedAttack : "All Cyber") +" Attacks in "+ selectedYear},
    datalabels: severityChartType === "pie" ? {
     color:"#fff",
     formatter:(v,ctx)=>{
      const arr = ctx.chart.data.datasets[0].data;
      const total = arr.reduce((a,b)=>a+b,0);
      return ((v/total)*100).toFixed(1)+" % - "+v;
     }
    } : false
   }
  }
});
}

async function loadMitigation(){
 if(!selectedYear || !selectedAttack) return;

 const res = await fetch(`http://localhost:8000/cyber/mitigation?year=${selectedYear}&attack=${encodeURIComponent(selectedAttack)}`);
 const data = await res.json();

 mitigationData = data.mitigations || [];

 await tick();
 drawMitigationChart();
 saveLocal();
}

async function loadOutcome(){
 if(!selectedYear || !selectedAttack) return;

 const res = await fetch(`http://localhost:8000/cyber/outcome?year=${selectedYear}&attack=${encodeURIComponent(selectedAttack)}`);
 const data = await res.json();

 if(data.error){
  outcomeData = [];
 }else{
  outcomeData = [
   { label: "Success", value: data.success_percent },
   { label: "Failure", value: data.failure_percent }
  ];
 }

 await tick();
 drawOutcomeChart();
 saveLocal();
}

function drawMitigationChart(){
 if(!mitigationCanvas || mitigationData.length === 0) return;
 if(mitigationChart) mitigationChart.destroy();

 mitigationChart = new Chart(mitigationCanvas,{
  type: mitigationChartType,
  data:{
   labels: mitigationData.map(d=>d.mitigation_method),
   datasets:[{
    label: "Mitigation Effectiveness on " + selectedAttack,
    data: mitigationData.map(d=>d.count),
    backgroundColor: mitigationChartType === "pie" ? pieColors : "#faad55"
   }]
  },
  options:{
   responsive:true,
   maintainAspectRatio:false,
   plugins:{
    legend:{display:true},
    title:{display:true,text:selectedAttack+" Mitigation Methods in "+selectedYear},
    datalabels: mitigationChartType === "pie" ? {
     color:"#fff",
     font:{weight:"bold"},
     formatter:(v,ctx)=>{
      const arr = ctx.chart.data.datasets[0].data;
      const total = arr.reduce((a,b)=>a+b,0);
      return ((v/total)*100).toFixed(1)+"% ( "+v+" )";
     }
    } : false
   }
  }
 });
}

function drawOutcomeChart(){
 if(!outcomeCanvas || outcomeData.length === 0) return;
 if(outcomeChart) outcomeChart.destroy();

 outcomeChart = new Chart(outcomeCanvas,{
  type: outcomeChartType,
  data:{
   labels: outcomeData.map(d=>d.label),
   datasets:[{
    label: selectedAttack +" Attack Outcome",
    data: outcomeData.map(d=>d.value),
    backgroundColor: outcomeChartType === "pie" ? pieColors : "#64c6ed"
   }]
  },
  options:{
   responsive:true,
   maintainAspectRatio:false,
   plugins:{
    legend:{display:true},
    title:{display:true,text:selectedAttack+" Outcome Rate in "+selectedYear},
    datalabels: outcomeChartType === "pie" ? {
     color:"#fff",
     font:{weight:"bold"},
     formatter:(v,ctx)=>{
      return v+" %";
     }
    } : false
   }
  }
 });
}

function exportAttackPNG(){
 if(!attackChart) return;
 const safeAttack = selectedAttack ? selectedAttack.replace(/\s+/g,"_") : "Attack";
 const a=document.createElement("a");
 a.href=attackChart.toBase64Image();
 a.download=`Cyber_Attack_Trend_${safeAttack}.png`;
 a.click();
}

function exportIndustryPNG(){
 if(!industryChart) return;
 const safeYear = selectedYear || "Year";
 const safeAttack = selectedAttack ? selectedAttack.replace(/\s+/g,"_") : "All attacks";
 const a=document.createElement("a");
 a.href=industryChart.toBase64Image();
 a.download=`Industry_Impact_${safeYear}_${safeAttack}.png`;
 a.click();
}

function exportTargetPNG(){
 if(!targetChart) return;
 const safeAttack = selectedAttack ? selectedAttack.replace(/\s+/g,"_") : "Attack";
 const safeHour = selectedHour !== "" ? selectedHour : "Hour";
 const a=document.createElement("a");
 a.href=targetChart.toBase64Image();
 a.download=`Cyber_Target_Systems_${safeAttack}_${safeHour}.png`;
 a.click();
}

function exportDataLossPNG(){
 if(!dataLossChart) return;
 const safeIndustry = selectedIndustry ? selectedIndustry.replace(/\s+/g,"_") : "All";
 const a=document.createElement("a");
 a.href=dataLossChart.toBase64Image();
 a.download=`Cyber_Data_Loss_${safeIndustry}.png`;
 a.click();
}

function exportSeverityPNG(){
 if(!severityChart) return;
 const safeYear = selectedYear || "Year";
 const safeAttack = selectedAttack ? selectedAttack.replace(/\s+/g,"_") : "All";
 const a=document.createElement("a");
 a.href=severityChart.toBase64Image();
 a.download=`Cyber_Severity_${safeYear}_${safeAttack}.png`;
 a.click();
}

function exportMitigationPNG(){
 if(!mitigationChart) return;
 const safeYear = selectedYear || "Year";
 const safeAttack = selectedAttack ? selectedAttack.replace(/\s+/g,"_") : "Attack";
 const a=document.createElement("a");
 a.href=mitigationChart.toBase64Image();
 a.download=`Cyber_Mitigation_${safeYear}_${safeAttack}.png`;
 a.click();
}

function exportOutcomePNG(){
 if(!outcomeChart) return;
 const safeYear = selectedYear || "Year";
 const safeAttack = selectedAttack ? selectedAttack.replace(/\s+/g,"_") : "Attack";
 const a=document.createElement("a");
 a.href=outcomeChart.toBase64Image();
 a.download=`Cyber_Outcome_${safeYear}_${safeAttack}.png`;
 a.click();
}

function clearAttack() {
    selectedAttack = "";
    attackTrendData = [];

    if (attackChart) {
        attackChart.destroy();
    }

    attackChart = null;
    sessionStorage.clear();
}

function clearSection2(){
 selectedAttack = "";
 selectedYear="";
 selectedHour="";
 industryData=[];
 targetData=[];
 if(industryChart) industryChart.destroy();
 if(targetChart) targetChart.destroy();
 industryChart=null;
 targetChart=null;
 sessionStorage.clear();
}

function clearSection3(){
 selectedAttack = "";
 selectedIndustry="";
 selectedYear="";
 severityData=[];
 dataLossData=[];
 if(dataLossChart) dataLossChart.destroy();
 if(severityChart) severityChart.destroy();
 dataLossChart=null;
 severityChart=null;
 sessionStorage.clear();
}

function clearSection4(){
 selectedAttack = "";
 selectedYear = "";
 mitigationData = [];
 outcomeData = [];

 if(mitigationChart) mitigationChart.destroy();
 if(outcomeChart) outcomeChart.destroy();

 mitigationChart = null;
 outcomeChart = null;
 sessionStorage.clear();
}

onMount(async ()=>{
 loadLocal();
 await loadDropdowns();
 await tick();
 resizeAll();
 resizeContinuously();
 drawAttackChart();
 drawIndustryChart();
 drawTargetChart();
 drawSeverityChart();
 drawDataLossChart();
 drawMitigationChart();
 drawOutcomeChart();
 
});
</script>

<main class="cyber">

<section class="block">
<div class="header">
<h2>Cyber Attacks Overview</h2>

<div class="right-controls">

<select bind:this={attackSelect} bind:value={selectedAttack} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">Select Attack Type</option>
{#each attackTypes as a}<option>{a}</option>{/each}
</select>

{#if attackTrendData.length>0}
<select bind:this={attackTypeSelect} bind:value={attackChartType} on:change={(e)=>{autoResizeSelect(e.target); drawAttackChart();}}>
<option value="pie">Pie</option>
<option value="line">Line</option>
<option value="bar">Bar</option>
</select>
{/if}

<button on:click={loadAttackTrend}>Load</button>
<button on:click={exportAttackPNG}>Export</button>
<button on:click={clearAttack} class="clear">Clear</button>

</div>
</div>

{#if attackTrendData.length>0}
<div class="chart-box fade">
<canvas bind:this={attackCanvas}></canvas>
</div>
{/if}
</section>

<section class="block">

<div class="header">
<h2>Industry & Target Analysis</h2>

<div class="right-controls">

<div class="toggle-wrap">
<span class:active={!isTargetMode}>Industry</span>
<label class="toggle">
<input type="checkbox" bind:checked={isTargetMode} on:change={saveLocal}>
<span class="slider"></span>
</label>
<span class:active={isTargetMode}>Targets</span>
</div>

{#if !isTargetMode}

<select bind:this={yearSelect} bind:value={selectedYear} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">Select Year</option>
{#each years as y}<option value={y}>{y}</option>{/each}
</select>

<select bind:this={attackFilterSelect} bind:value={selectedAttack} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">All Attacks</option>
{#each attackTypes as a}<option>{a}</option>{/each}
</select>

{#if industryData.length>0}
<select bind:this={industryTypeSelect} bind:value={industryChartType} on:change={(e)=>{autoResizeSelect(e.target); drawIndustryChart();}}>
<option value="bar">Bar</option>
<option value="pie">Pie</option>
</select>
{/if}

<button on:click={loadIndustry}>Load</button>
<button on:click={exportIndustryPNG}>Export</button>
<button class="clear" on:click={clearSection2}>Clear</button>

{:else}

<select bind:value={selectedAttack} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">Select Attack Type</option>
{#each attackTypes as a}<option>{a}</option>{/each}
</select>

<input type="number" on:change={loadTargets}  bind:value={selectedHour} min="0" max="23" placeholder="Hour (0-23)" style="width:85px">

{#if targetData.length>0}
<select bind:this={targetTypeSelect} bind:value={targetChartType} on:change={(e)=>{autoResizeSelect(e.target); drawTargetChart();}}>
<option value="bar">Bar</option>
<option value="pie">Pie</option>
</select>
{/if}

<button on:click={loadTargets}>Load</button>
<button on:click={exportTargetPNG}>Export</button>
<button class="clear" on:click={clearSection2}>Clear</button>

{/if}

</div>
</div>

{#if industryData.length>0}
<div class="chart-box fade" style="display:{isTargetMode ? 'none' : 'block'}">
<canvas bind:this={industryCanvas}></canvas>
</div>
{/if}

{#if targetData.length>0}
<div class="chart-box fade" style="display:{isTargetMode ? 'block' : 'none'}">
<canvas bind:this={targetCanvas}></canvas>
</div>
{/if}

</section>
<section class="block">

<div class="header">
<h2>Data Loss & Severity Analysis</h2>

<div class="right-controls">

<div class="toggle-wrap">
<span class:active={!isSeverityMode}>Data Loss</span>
<label class="toggle">
<input type="checkbox" bind:checked={isSeverityMode} on:change={saveLocal}>
<span class="slider"></span>
</label>
<span class:active={isSeverityMode}>Severity</span>
</div>

{#if !isSeverityMode}

<select bind:this={industrySelect3} bind:value={selectedIndustry} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">All Industries</option>
{#each industries as i}<option>{i}</option>{/each}
</select>

{#if dataLossData.length>0}
<select bind:this={dataLossTypeSelect} bind:value={dataLossChartType} on:change={(e)=>{autoResizeSelect(e.target); drawDataLossChart();}}>
<option value="pie">Pie</option>
<option value="bar">Bar</option>
</select>
{/if}

<button on:click={loadDataLoss}>Load</button>
<button on:click={exportDataLossPNG}>Export</button>
<button class="clear" on:click={clearSection3}>Clear</button>

{:else}

<select bind:this={severityYearSelect} bind:value={selectedYear} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">Select Year</option>
{#each years as y}<option value={y}>{y}</option>{/each}
</select>

<select bind:this={severityAttackSelect} bind:value={selectedAttack} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">All Attacks</option>
{#each attackTypes as a}<option>{a}</option>{/each}
</select>

{#if severityData.length>0}
<select bind:this={severityTypeSelect} bind:value={severityChartType} on:change={(e)=>{autoResizeSelect(e.target); drawSeverityChart();}}>
<option value="pie">Pie</option>
<option value="bar">Bar</option>
</select>
{/if}

<button on:click={loadSeverity}>Load</button>
<button on:click={exportSeverityPNG}>Export</button>
<button class="clear" on:click={clearSection3}>Clear</button>

{/if}

</div>
</div>

{#if dataLossData.length>0}
<div class="chart-box fade" style="display:{isSeverityMode ? 'none' : 'block'}">
<canvas bind:this={dataLossCanvas}></canvas>
</div>
{/if}

{#if severityData.length>0}
<div class="chart-box fade" style="display:{isSeverityMode ? 'block' : 'none'}">
<canvas bind:this={severityCanvas}></canvas>
</div>
{/if}

</section>

<section class="block">

<div class="header">
<h2>Mitigation methods & Outcome Analysis</h2>

<div class="right-controls">

<div class="toggle-wrap">
<span class:active={!isDefenseMode}>Mitigation</span>
<label class="toggle">
<input type="checkbox" bind:checked={isDefenseMode} on:change={saveLocal}>
<span class="slider"></span>
</label>
<span class:active={isDefenseMode}>Outcome</span>
</div>

{#if !isDefenseMode}

<select bind:this={defenseYearSelect} bind:value={selectedYear} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">Select Year</option>
{#each years as y}<option value={y}>{y}</option>{/each}
</select>

<select bind:this={defenseAttackSelect} bind:value={selectedAttack} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">Select Attack Type</option>
{#each attackTypes as a}<option>{a}</option>{/each}
</select>

{#if mitigationData.length>0}
<select bind:this={mitigationTypeSelect} bind:value={mitigationChartType} on:change={(e)=>{autoResizeSelect(e.target); drawMitigationChart();}}>
<option value="bar">Bar</option>
<option value="pie">Pie</option>
</select>
{/if}

<button on:click={loadMitigation}>Load</button>
<button on:click={exportMitigationPNG}>Export</button>
<button class="clear" on:click={clearSection4}>Clear</button>

{:else}

<select bind:value={selectedYear} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">Select Year</option>
{#each years as y}<option value={y}>{y}</option>{/each}
</select>

<select bind:value={selectedAttack} on:change={(e)=>autoResizeSelect(e.target)}>
<option value="">Select Attack Type</option>
{#each attackTypes as a}<option>{a}</option>{/each}
</select>

{#if outcomeData.length>0}
<select bind:this={outcomeTypeSelect} bind:value={outcomeChartType} on:change={(e)=>{autoResizeSelect(e.target); drawOutcomeChart();}}>
<option value="pie">Pie</option>
<option value="bar">Bar</option>
</select>
{/if}

<button on:click={loadOutcome}>Load</button>
<button on:click={exportOutcomePNG}>Export</button>
<button class="clear" on:click={clearSection4}>Clear</button>

{/if}

</div>
</div>

{#if mitigationData.length>0}
<div class="chart-box fade" style="display:{isDefenseMode ? 'none' : 'block'}">
<canvas bind:this={mitigationCanvas}></canvas>
</div>
{/if}

{#if outcomeData.length>0}
<div class="chart-box fade" style="display:{isDefenseMode ? 'block' : 'none'}">
<canvas bind:this={outcomeCanvas}></canvas>
</div>
{/if}

</section>

</main>

<style>
main.cyber{padding:25px}

.block{
background:white;
padding:20px;
border-radius:14px;
margin-top:60px;
transition:.3s;
}
.block:hover{
transform:translateY(-4px);
box-shadow:0 10px 25px rgba(0,0,0,.08);
}

.header{
display:flex;
justify-content:space-between;
align-items:center;
}

.right-controls{
display:flex;
gap:10px;
flex-wrap:wrap;
}

select,input{
padding:8px 14px;
border-radius:10px;
border:1px solid #ddd;
min-width:50px;
max-width:180px;
}

button{
background:#13b789;
color:white;
border:none;
padding:8px 14px;
border-radius:10px;
}
button:hover{transform:scale(1.05)}
button.clear{background:#e74c3c}

.chart-box{height:400px;margin-top:25px}

.fade{animation:fadeIn .4s ease}

@keyframes fadeIn{
from{opacity:0;transform:translateY(10px)}
to{opacity:1;transform:translateY(0)}
}

.toggle-wrap{
display:flex;
align-items:center;
gap:8px;
font-weight:600;
}

.toggle-wrap span{
opacity:.5;
transition:.3s;
}

.toggle-wrap span.active{
opacity:1;
transform:scale(1.05);
}

.toggle-wrap span:first-child.active{
color:#ff9933;
}

.toggle-wrap span:last-child.active{
color:#13b789;
}

.toggle{
position:relative;
display:inline-block;
width:50px;
height:24px;
}

.toggle input{display:none}

.slider{
position:absolute;
cursor:pointer;
top:0;left:0;right:0;bottom:0;
background:#ff9832;
border-radius:24px;
transition:.3s;
}
.slider:before{
position:absolute;
content:"";
height:18px;width:18px;
left:3px;bottom:3px;
background:white;
border-radius:50%;
transition:.3s;
}
input:checked + .slider{
background:#13b789;
}
input:checked + .slider:before{
transform:translateX(26px);
}
</style>
