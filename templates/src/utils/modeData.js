//假设为 modeData.js  到处数据，或者公用变量也可以
var testData = {
  num:1,
  handleNum: function(i){
    this.num = i
  }
}
//可多个数据
export default {testData}