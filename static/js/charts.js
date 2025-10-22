// Charts initialization for stats page
document.addEventListener('DOMContentLoaded', function(){
  // Fetch category stats from API and render pie
  async function loadCategoryChart(){
    try{
      const res = await fetch('/api/stats/category');
      const json = await res.json();
      if(!json.success) return;
      const labels = json.data.map(d=>d.category);
      const data = json.data.map(d=>d.total);
      const colors = ['#3b82f6','#60a5fa','#f97316','#f472b6','#10b981'];
      const ctx = document.getElementById('pieChart');
      if(ctx){ new Chart(ctx, { type:'pie', data: { labels, datasets:[{ data, backgroundColor: colors }] }, options:{ responsive:true, plugins:{ legend:{ position:'bottom' } } } }); }
    }catch(e){ console.warn('Category chart error', e); }
  }

  async function loadMonthlyChart(){
    try{
      const res = await fetch('/api/stats/monthly');
      const json = await res.json();
      if(!json.success) return;
      const labels = json.data.map(d=>d.month);
      const data = json.data.map(d=>d.total);
      const ctx = document.getElementById('barChart');
      if(ctx){ new Chart(ctx, { type:'bar', data: { labels, datasets:[{ label:'Spending', data, backgroundColor:'rgba(59,130,246,0.9)', borderRadius:6 }] }, options:{ responsive:true, scales:{ y:{ beginAtZero:true } } } }); }
    }catch(e){ console.warn('Monthly chart error', e); }
  }

  loadCategoryChart();
  loadMonthlyChart();

  // Trigger countups if present
  if(window.CountUp){
    document.querySelectorAll('.countup').forEach(el =>{
      const target = parseFloat(el.getAttribute('data-target')) || 0;
      try{ const cnt = new CountUp.CountUp(el, target, {duration:1.2, separator:',', prefix:'₹ '}); if(!cnt.error) cnt.start(); }catch(e){}
    });
  }

});
