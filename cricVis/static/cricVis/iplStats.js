google.charts.load("current", {packages: ['corechart', 'bar']});

function convertDataToMatrix(data,headers){
  let matrixData = []
  matrixData.push(headers);
  for (let xAxis in data){
    matrixData.push[xAxis, data[xAxis]];
  }
  return matrixData;
}

function receiveData(allIPLData){
  console.log(allIPLData);
}