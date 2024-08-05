 Here's the JavaScript code for checking if a number is an Armstrong number or not:

```javascript
// take input from the user
let num = 173;

// initialize sum
let sum = 0;

// find the sum of the cube of each digit
let temp = num;
while (temp > 0) {
   let digit = temp % 10;
   sum += Math.pow(digit, 3);
   temp = Math.floor(temp / 10);
}

// display the result
if (num === sum) {
   console.log(num, "is an Armstrong number");
} else {
   console.log(num, "is not an Armstrong number");
}
```

This code uses the `Math.pow()` function to calculate the cube of a digit and `Math.floor()` to get the integer part of a number. The rest of the logic remains the same as the Python code.