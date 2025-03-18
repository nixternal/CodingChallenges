const fs = require('fs');

/*****************************************************************************
 * Read puzzle input, this is such a goofy way, but this is what Google Gemini
 * gave me when I googled how to do this.
 *****************************************************************************/
readInput('../input.txt')
  .then(data => {
    let d = [];
    let left = [];
    let right = [];
    for (line of data.split('\n')) {
      d.push(line);
    }
    for (line of d) {
      const[l, r] = line.split('   ');
      if (l != '' && r != '') {
        left.push(l);
        right.push(r);
      }
    }
    console.log("Part 1:", partOne(left, right)); // 1530215
    console.log("Part 2:", partTwo(left, right)); // 26800609
  })
  .catch(err => {
    console.error('Error reading file:', err);
  });

function readInput(fin) {
  return new Promise((resolve, reject) => {
    fs.readFile(fin, 'utf8', (err, data) => {
      if (err) {
        reject(err);
      } else {
        resolve(data);
      }
    });
  });
}

/*****************************************************************************
 * Part 1 of the puzzle, read the other documentation from either the Python or
 * Golang code.
 *****************************************************************************/
function partOne(left, right) {
  let sum = 0;
  left.sort();
  right.sort();
  for (i = 0; i < left.length; i++) {
    sum += Math.abs(Number(left[i]) - Number(right[i]));
  }
  return sum;
}

/*****************************************************************************
 * Part 2 of the puzzle, read the other documentation from either the Python or
 * Golang code.
 *****************************************************************************/
function partTwo(left, right) {
  let sum = 0;
  for (const x of left) {
    sum += Number(x) * right.filter(element => element === x).length;
  }
  return sum;
}
