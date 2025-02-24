

async function get_data(){
    let res = await fetch("http://127.0.0.1:5000/data");
    let jsonData = await res.json();
    return await parser_data(jsonData)
}

async function create_table(){
    //define table
    d = await get_data() 
    var table = new Tabulator("#example-table", {
        data:d,
        autoColumns:true,
    });}


function parser_data(json){
    res = []
    for (let computer in json){
        for (let inx in json[computer]){
            decryp_text = xorDecrypt(json[computer][inx]["data"])
            console.log(decryp_text)
            res.push({computer: computer, time : json[computer][inx]["time"],data: decryp_text})
        } 
    }
    return res
}

function xorDecrypt(data, key = "my_secret_key") {
    return data.split('').map((c, i) => 
        String.fromCharCode(c.charCodeAt(0) ^ key.charCodeAt(i % key.length))
    ).join('');
}
