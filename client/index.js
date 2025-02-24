function handleIt(){
    const params = new URLSearchParams({
            computer: computer.value,
            startDate: startDate.value,
            enDate: endDate.value,
            startTime: startTime.value,
            startDate: endTime.value
    })
    fetch(`http://127.0.0.1:5000/data?${params.toString()}`)
    .then(res => res.json())  // Parse JSON from the response
    .then(data => {
        for (var com in data){
            console.log(data[com])
            for (let i = 0; i< data[com].length; i++){
                console.log(data[com][i])
            } 
        }
        // console.log(data);  // Log the actual JSON data
        show_table();  // Redirect only after fetching the data
    })
    .catch(error => console.error("Error fetching data:", error));
}
function show_table(){
    // console.log(data[0]);
    window.location.href = "table.html";
    tableCreate();

}

function tableCreate() {
    const body = document.body,
          tbl = document.createElement('table');
    tbl.style.width = '100px';
    tbl.style.border = '1px solid black';
  
    for (let i = 0; i < 3; i++) {
      const tr = tbl.insertRow();
      for (let j = 0; j < 2; j++) {
        if (i === 2 && j === 1) {
          break;
        } else {
          const td = tr.insertCell();
          td.appendChild(document.createTextNode(`Cell I${i}/J${j}`));
          td.style.border = '1px solid black';
          if (i === 1 && j === 1) {
            td.setAttribute('rowSpan', '2');
          }
        }
      }
    }
    body.appendChild(tbl);
  }
  
