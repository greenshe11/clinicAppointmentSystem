

function smithWaterman(s1,s2){
  const match = 2;
  const mismatch = -1;
  const gap = -1;

  const rows = s1.length + 1;
  const cols = s2.length + 1;
  let distance = 0
  let values = []
  let firstScore = true
  
  function calculate_score(matrix, x, y) {
      /* Calculates score for given coordinate in matrix. */

      // compute similarity score
      let similarity = (s1[x-1] == s2[y-1]) ? match : mismatch;
     
      // compute diagonal, above, and left scores
      let score_diag = matrix[x-1][y-1] + similarity;
      let score_above = matrix[x-1][y] + gap;
      let score_left = matrix[x][y-1] + gap;

      const array = [score_diag, score_above, score_left]
      const max= Math.max(score_diag, score_above, score_left);
      
      const i = array.indexOf(max)
      values.push(i)
      if (i==0){
        if (similarity==2){
          if (firstScore){
            distance +=0.5
          }
          distance+=1
        }
        if (similarity==-1){
  
          distance-=1
        }
      }
      firstScore = false
      
      return max
      
  }

  function create_matrix(rows, cols) {
      /* Create scoring matrix */

      // initialize matrix with 0s
      let score_matrix = [];
      for (let i = 0; i < rows; i++) {
          score_matrix[i] = [];
          for (let j = 0; j < cols; j++) {
              score_matrix[i].push(0);
          }
      }

      // compute scores and fill matrix
      let max_score = 0;
      let max_coords = [0,0];
      for (let i = 1; i < rows; i++) {
        
          for (let j = 1; j < cols; j++) {
            
              let score = calculate_score(score_matrix, i, j);
              if (score > max_score) {
                  max_score = score;
                  max_coords = [i,j];
              }
              score_matrix[i][j] = score;
          }
      }
      
      return [score_matrix, max_coords];
  }

  function next_move(score_matrix, x, y) {
      /* Determine next move during traceback */

      let diag = score_matrix[x - 1][y - 1];
      let up   = score_matrix[x - 1][y];
      let left = score_matrix[x][y - 1];

      if ((diag >= up) && (diag >= left)) {
          if (diag != 0) return 1;
          else return 0;
      } else if ((up > diag) && (up >= left)) {
          if (up != 0) return 2;
          else return 0;
      } else if ((left > diag) && (left > up)) {
          if (left != 0) return 3;
          else return 0;
      } else {
          return 0;
      }

  }
  

  function traceback(score_matrix, start_coord) {
      let end = 0;
      let diag = 1;
      let up = 2;
      let left = 3;
      let s1_aligned = [];
      let s2_aligned = [];
      let x = start_coord[0];
      let y = start_coord[1];
      let move = next_move(score_matrix, x, y);

      while (move != end) {
          if (move == diag) {
              s1_aligned.push(s1[x-1]);
              s2_aligned.push(s2[y-1]);
              x--;
              y--;
          } else if (move == up) {
              s1_aligned.push(s1[x-1]);
              s2_aligned.push('-');
              x--;
          } else {
              s1_aligned.push('-');
              s2_aligned.push(s2[y-1]);
              y--;
          }
          move = next_move(score_matrix, x, y);
      }

      s1_aligned.push(s1[x-1]);
      s2_aligned.push(s2[y-1]);

      return [s1_aligned.reverse(), s2_aligned.reverse()];
  }

  let m = create_matrix(rows,cols)
  let res= rows-distance
  return res
}

class WordSuggestions{
  constructor(wordBag){
    this.wordBag = wordBag
    this.evaluateInput('')
    this.symptoms = []
  }

  editDistance(a, b){
    function customCheck(a, b) {
      return a === b;
  }
    const updateCost = 1 // changing
    const insertCost = 0 // missing
    const deletionCost =1 // removing / excess

    var t = [], u, i, j, m = a.length, n = b.length;
    if (!m) { return n; }
    if (!n) { return m; }
    for (j = 0; j <= n; j++) { t[j] = j; }
    for (i = 1; i <= m; i++) {
        for (u = [i], j = 1; j <= n; j++) {
            u[j] = customCheck(a[i - 1], b[j - 1]) ? t[j - 1] : Math.min(t[j - 1] + updateCost, t[j] + deletionCost, u[j - 1] + insertCost); 
        } t = u;
    } return u[n];
}



    getOverallDistancel(word, wordBasis, func){
      let wordArray = wordBasis.split(' ')
      wordArray.push(wordBasis)
      let leastNum = null
      for (let i=0; i<wordArray.length; i++){
        const key = wordArray[i].toLowerCase()
        
        let distance = func(word, key)
        if (leastNum==null){
          leastNum = distance
        }
        if (distance<leastNum){
          leastNum = distance
        }
      }
      return leastNum


      
      
    }
    
    getNearestWord(word,  data=null){
      if(!data){
        data = this.wordBag
      }

      const func = smithWaterman
      const distances = {}
      for (let i=0; i<data.length; i++){
        const key = data[i]
        distances[key] = this.getOverallDistancel(word, key, func)//this.getOverallDistancel(word, key)
        
      }
      const sortedEntries = Object.entries(distances).sort(([, valueA], [, valueB]) => valueA - valueB);
      
      const getOutput = (key, value, returnValue)=> {
        if(returnValue){
          return value
        }else{
          return key
        }
        
      }

      let res = sortedEntries.slice(0, sortedEntries.length)
      let finalList = []
      let resValues = res.map(([key,value]) => getOutput(key,value,true))
      let resNames = res.map(([key,value]) => getOutput(key,value, false)) // Extract the keys
     
      const topValue = resValues[0]
      let benchmark = topValue*1.5
      if (topValue<0){
        benchmark = topValue/1.5
      }

      for (let i=0;i<resValues.length;i++){
        
        if ((resValues[i]<=benchmark || resValues[i]<5)){
          finalList.push(resNames[i])
        }
      }

      return finalList
      
      
    }

  evaluateInput(){
    const word = document.getElementById("textbox").value.toLowerCase();
   
    const symptomsSuggested = this.getNearestWord(word)
    const suggestionList = document.getElementById('symptoms-suggestion-list');
    
    // Populate the suggestion list
    suggestionList.innerHTML = ''
    symptomsSuggested.forEach(symptom => {
        const li = document.createElement('li');
        li.textContent = symptom;
        li.classList.add('dropdown-item')
  

        li.onclick = ()=>{this.addToSelectedSymptoms(li)}
        //this.addToSelectedSymptoms(li)
        suggestionList.appendChild(li);
    });
  }
  removeSymptomTag(parent, element){
    parent.removeChild(element)
    this.updateTags(parent)

    
  }
  updateTags(element){
    element.childNodes.forEach(symptom => {
      this.symptoms.push(symptom.textContent)
    this.symptoms = [...new Set(this.symptoms)];
    });
  }
  addToSelectedSymptoms(element){
    console.log('selected', element.textContent)
    const targetElement = document.getElementById('symptom-tags-list')
    element.textContent
    let tag = document.createElement('div')
    tag.textContent = element.textContent
    tag.classList.add('symptom-tag')
    tag.onclick = () => {
      this.removeSymptomTag(targetElement, tag)
    }
    targetElement.append(tag)
    this.symptoms = []
    this.updateTags(targetElement)
    console.log(this.symptoms)



  }
}

const leven = new WordSuggestions(
  [
    'Ringing of Ears',
    'san mig',
    'creamier',
    'del monte',
    'sweet chili',
    'bubble',
    'pitcher',
    'fever',
    'high temperature',
    'low temperature',
    'Over 40 degrees body temperature'
  ]
)
window.suggestSymptoms = leven.evaluateInput.bind(leven)
window.addToSelectedSymptoms = leven.addToSelectedSymptoms.bind(leven)
window.removeSymptomTag = leven.removeSymptomTag.bind(leven)

console.log('ghee')