function handleIt(){
    console.log(123456);
    // // a = document.getElementById('endTime').value
    // console.log(computer.value)
    
    // getText()
    try {
        const params = new URLSearchParams({
            computer: computer.value,
            startDate: startDate.value,
            enDate: endDate.value,
            startTime: startTime.value,
            startDate: endTime.value
        })
        fetch(`http://127.0.0.1:5000/data?${params.toString()}`)
        .then(res => res.json())  // Parse JSON from the response
        .then(data => console.log(data))  // Log the actual JSON data
        .catch(error => console.error("Error fetching data:", error));  // Handle errors
    
        //   .then(recordset => recordset.json())
        //   .then(results => {
        //     this.setState({ AccountDetails: results.recordset });
        //   });
      } catch (e) {
        console.log(e);
      }
}



async function getText() {
    // let myObject = await fetch('http://127.0.0.1:5000');
    // let myText = await myObject.text();
    // console.log(myText)
    // var payload = {
    //     computer : computer.value,
    //     startDate: startDate.value,
    //     endDate: endDate.value,
    //     startTime: startTime.value,
    //     endTime: endTime.value
    //     // 1:2,
    //     // 2:3
    // };
    var payload = {
        a: 1,
        b: 2
    };
   
    
    var data = new FormData();
    data.append( "json", JSON.stringify( payload ) );
    
    fetch('http://127.0.0.1:5000/data',
    {
        method: "POST",
        body: data
    })
    .then(function(res){ return res.json(); })
    .then(function(data){ alert( JSON.stringify( data ) ) })
  }