# JavaScript Exercises: From Beginner to Advanced

> Học đi đôi với hành - Code mỗi ngày để thành thạo

---

## 📑 Mục lục

1. [Level 1: Beginner (Weeks 1-4)](#level-1-beginner)
2. [Level 2: Intermediate (Weeks 5-8)](#level-2-intermediate)
3. [Level 3: Advanced (Weeks 9-12)](#level-3-advanced)
4. [Level 4: Expert (Weeks 13+)](#level-4-expert)
5. [Project Challenges](#project-challenges)
6. [Solutions](#solutions)

---

## Level 1: Beginner

### 1.1 Variables & Data Types

**Bài 1: Khai báo biến**
```javascript
// ✅ Yêu cầu:
// 1. Khai báo hằng số PI = 3.14159
// 2. Khai báo biến name = "Alice"
// 3. Khai báo biến age = 25
// 4. Khai báo biến isStudent = true

// 📝 Code của bạn:


// ✅ Test:
console.log(PI); // 3.14159
console.log(name); // "Alice"
console.log(typeof age); // "number"
console.log(isStudent); // true
```

**Bài 2: Template literals**
```javascript
// ✅ Yêu cầu: Tạo greeting string dùng template literal
// Output: "Hello, my name is Alice and I'm 25 years old"

const name = "Alice";
const age = 25;

// 📝 Code của bạn:


// ✅ Test:
console.log(greeting);
```

**Bài 3: Type conversion**
```javascript
// ✅ Yêu cầu:
// 1. Convert string "42" thành number
// 2. Convert number 100 thành string
// 3. Convert empty string "" thành boolean
// 4. Convert string "hello" thành boolean

// 📝 Code của bạn:


// ✅ Test:
console.log(typeof numStr); // "number"
console.log(typeof strNum); // "string"
console.log(boolEmpty); // false
console.log(boolHello); // true
```

---

### 1.2 Operators

**Bài 4: Toán tử so sánh**
```javascript
// ✅ Yêu cầu: Dự đoán kết quả
const a = 5;
const b = "5";

console.log(a == b);  // ?
console.log(a === b); // ?
console.log(a != b);  // ?
console.log(a !== b); // ?

// Giải thích:
```

**Bài 5: Nullish coalescing**
```javascript
// ✅ Yêu cầu: Dùng ?? để set default value
const userInput = null;
const defaultValue = "Guest";

// 📝 Code của bạn:
const name = null;

// ✅ Test:
console.log(name); // "Guest"

// Thử với empty string:
const userInput2 = "";
const name2 = userInput2 ?? defaultValue;
console.log(name2); // "" (empty string vẫn được dùng)
```

---

### 1.3 Conditionals

**Bài 6: Kiểm tra số chẵn/lẻ**
```javascript
// ✅ Yêu cầu: Viết hàm kiểm tra số chẵn hay lẻ
function checkEvenOdd(num) {
  // 📝 Code của bạn:

}

// ✅ Test:
console.log(checkEvenOdd(4));  // "Even"
console.log(checkEvenOdd(7));  // "Odd"
console.log(checkEvenOdd(0));  // "Even"
```

**Bài 7: Xếp loại học lực**
```javascript
// ✅ Yêu cầu: Viết hàm xếp loại dựa trên điểm
// 90-100: "Excellent"
// 80-89: "Good"
// 70-79: "Fair"
// 60-69: "Pass"
// 0-59: "Fail"

function gradeStudent(score) {
  // 📝 Code của bạn:

}

// ✅ Test:
console.log(gradeStudent(95)); // "Excellent"
console.log(gradeStudent(85)); // "Good"
console.log(gradeStudent(50)); // "Fail"
```

**Bài 8: Ternary operator**
```javascript
// ✅ Yêu cầu: Viết lại dùng ternary operator
function getDiscount(isMember) {
  // 📝 Code của bạn:

}

// ✅ Test:
console.log(getDiscount(true));  // 0.1
console.log(getDiscount(false)); // 0
```

---

### 1.4 Loops

**Bài 9: Tính tổng từ 1 đến n**
```javascript
// ✅ Yêu cầu: Viết hàm tính tổng
function sumToN(n) {
  // 📝 Code của bạn:

}

// ✅ Test:
console.log(sumToN(5));  // 15 (1+2+3+4+5)
console.log(sumToN(10)); // 55
```

**Bài 10: In ra số nguyên tố**
```javascript
// ✅ Yêu cầu: Viết hàm kiểm tra số nguyên tố
function isPrime(num) {
  // 📝 Code của bạn:

}

// ✅ Test:
console.log(isPrime(2));  // true
console.log(isPrime(17)); // true
console.log(isPrime(4));  // false
console.log(isPrime(1));  // false
```

**Bài 11: FizzBuzz**
```javascript
// ✅ Yêu cầu: In ra từ 1 đến 100
// - Chia hết cho 3: "Fizz"
// - Chia hết cho 5: "Buzz"
// - Chia hết cho cả 3 và 5: "FizzBuzz"
// - Còn lại: in ra số

function fizzBuzz() {
  // 📝 Code của bạn:

}

// ✅ Test (một phần):
// 1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz...
```

---

### 1.5 Functions

**Bài 12: Function expression vs Arrow**
```javascript
// ✅ Yêu cầu: Viết lại dùng arrow function
const multiply = function(a, b) {
  return a * b;
};

// 📝 Code của bạn:


// ✅ Test:
console.log(multiply(3, 4)); // 12
```

**Bài 13: Default parameters**
```javascript
// ✅ Yêu cầu: Viết hàm greet với default parameter
function greet(name = "Anonymous") {
  // 📝 Code của bạn:

}

// ✅ Test:
console.log(greet());        // "Hello, Anonymous!"
console.log(greet("Alice")); // "Hello, Alice!"
```

**Bài 14: Rest parameters**
```javascript
// ✅ Yêu cầu: Viết hàm tính tổng nhiều số
function sum(...numbers) {
  // 📝 Code của bạn:

}

// ✅ Test:
console.log(sum(1, 2, 3));       // 6
console.log(sum(1, 2, 3, 4, 5)); // 15
```

---

## Level 2: Intermediate

### 2.1 Arrays

**Bài 15: Array methods cơ bản**
```javascript
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// ✅ Yêu cầu:
// 1. Lọc ra số chẵn
// 2. Nhân đôi mỗi số
// 3. Tính tổng tất cả
// 4. Tìm số đầu tiên > 5

// 📝 Code của bạn:
const evenNumbers = null;
const doubled = null;
const total = null;
const firstGreaterThanFive = null;

// ✅ Test:
console.log(evenNumbers); // [2, 4, 6, 8, 10]
console.log(doubled);     // [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
console.log(total);       // 55
console.log(firstGreaterThanFive); // 6
```

**Bài 16: Chain array methods**
```javascript
const products = [
  { name: "Laptop", price: 1000, category: "Electronics" },
  { name: "Mouse", price: 25, category: "Electronics" },
  { name: "Desk", price: 200, category: "Furniture" },
  { name: "Chair", price: 150, category: "Furniture" },
  { name: "Keyboard", price: 75, category: "Electronics" }
];

// ✅ Yêu cầu:
// 1. Lọc products giá < 100
// 2. Map ra tên sản phẩm
// 3. Join thành string

// 📝 Code của bạn:
const cheapProducts = null;

// ✅ Test:
console.log(cheapProducts); // ["Mouse", "Desk", "Chair", "Keyboard"]
```

**Bài 17: Unique array**
```javascript
// ✅ Yêu cầu: Loại bỏ phần tử trùng lặp
function unique(arr) {
  // 📝 Code của bạn:

}

// ✅ Test:
console.log(unique([1, 2, 2, 3, 4, 4, 5])); // [1, 2, 3, 4, 5]
console.log(unique(["a", "b", "a", "c"]));  // ["a", "b", "c"]
```

---

### 2.2 Objects

**Bài 18: Object destructuring**
```javascript
const user = {
  name: "Alice",
  age: 25,
  email: "alice@email.com",
  address: {
    city: "Hanoi",
    country: "Vietnam"
  }
};

// ✅ Yêu cầu:
// 1. Extract name, age ra biến riêng
// 2. Extract city từ nested object
// 3. Extract email với default value nếu không có

// 📝 Code của bạn:


// ✅ Test:
console.log(name); // "Alice"
console.log(city); // "Hanoi"
```

**Bài 19: Object spread**
```javascript
// ✅ Yêu cầu: Merge objects không mutate object gốc
const defaults = { theme: "dark", lang: "en", notifications: true };
const userPrefs = { theme: "light", lang: "vi" };

// 📝 Code của bạn:
const finalPrefs = null;

// ✅ Test:
console.log(finalPrefs);
// { theme: "light", lang: "vi", notifications: true }
console.log(defaults.theme); // "dark" (không bị mutate)
```

**Bài 20: Object to array**
```javascript
// ✅ Yêu cầu: Chuyển object thành array of entries
const scores = { Alice: 90, Bob: 85, Charlie: 95 };

// 📝 Code của bạn:
const entriesArray = null;

// ✅ Test:
console.log(entriesArray);
// [["Alice", 90], ["Bob", 85], ["Charlie", 95]]
```

---

### 2.3 DOM & Events

**Bài 21: Toggle class**
```html
<!-- ✅ Yêu cầu: Click button để toggle class "active" trên div -->
<div id="box">Click the button!</div>
<button id="toggleBtn">Toggle</button>

<script>
// 📝 Code của bạn:

</script>
```

**Bài 22: Form validation**
```html
<!-- ✅ Yêu cầu: Validate form trước khi submit -->
<form id="loginForm">
  <input type="email" id="email" required>
  <input type="password" id="password" minlength="6" required>
  <button type="submit">Login</button>
</form>

<script>
// 📝 Code của bạn:
// - Email phải hợp lệ
// - Password ít nhất 6 ký tự
// - Hiển thị lỗi nếu không hợp lệ

</script>
```

**Bài 23: Event delegation**
```html
<!-- ✅ Yêu cầu: Dùng event delegation cho list -->
<ul id="list">
  <li class="item">Item 1</li>
  <li class="item">Item 2</li>
  <li class="item">Item 3</li>
</ul>

<script>
// 📝 Code của bạn:
// Click vào item nào thì log nội dung item đó

</script>
```

---

### 2.4 ES6+ Features

**Bài 24: Destructuring function params**
```javascript
// ✅ Yêu cầu: Viết hàm dùng destructuring
function createUser({ name, email, age = 18 }) {
  // 📝 Code của bạn:

}

// ✅ Test:
const user = createUser({ name: "Alice", email: "alice@email.com" });
console.log(user); // { name: "Alice", email: "alice@email.com", age: 18 }
```

**Bài 25: Template literals nâng cao**
```javascript
// ✅ Yêu cầu: Tạo tagged template để uppercase
function uppercase(strings, ...values) {
  // 📝 Code của bạn:

}

const name = "alice";
const result = uppercase`Hello, ${name}!`;

// ✅ Test:
console.log(result); // "HELLO, ALICE!"
```

---

## Level 3: Advanced

### 3.1 Closures & Scope

**Bài 26: Create counter với closure**
```javascript
// ✅ Yêu cầu: Tạo function trả về counter object
function createCounter() {
  // 📝 Code của bạn:

}

const counter = createCounter();
console.log(counter.increment()); // 1
console.log(counter.increment()); // 2
console.log(counter.decrement()); // 1
console.log(counter.getCount());  // 1
```

**Bài 27: Function factory**
```javascript
// ✅ Yêu cầu: Tạo function tạo ra multiplier functions
function createMultiplier(multiplier) {
  // 📝 Code của bạn:

}

const double = createMultiplier(2);
const triple = createMultiplier(3);

console.log(double(5)); // 10
console.log(triple(5)); // 15
```

---

### 3.2 this & bind

**Bài 28: Fix lost this**
```javascript
// ✅ Yêu cầu: Fix lỗi mất context this
const obj = {
  name: "Alice",
  greet() {
    console.log(`Hello, I'm ${this.name}`);
  }
};

const greetFunc = obj.greet;
greetFunc(); // ❌ undefined - Fix bằng bind!

// 📝 Code của bạn:

```

**Bài 29: Implement bind**
```javascript
// ✅ Yêu cầu: Tự implement bind function
Function.prototype.myBind = function(context, ...args) {
  // 📝 Code của bạn:

};

const obj = { name: "Alice" };
function greet(greeting) {
  console.log(`${greeting}, I'm ${this.name}`);
}

const bound = greet.myBind(obj, "Hello");
bound(); // "Hello, I'm Alice"
```

---

### 3.3 Prototypes & Classes

**Bài 30: Create class với inheritance**
```javascript
// ✅ Yêu cầu: Tạo class hierarchy
// Animal (base) → Dog (extends Animal)
// Animal: name, age, eat()
// Dog: breed, bark()

// 📝 Code của bạn:


// ✅ Test:
const dog = new Dog("Buddy", 3, "Golden");
console.log(dog.eat());  // "Buddy is eating"
console.log(dog.bark()); // "Woof! I'm Buddy"
```

**Bài 31: Prototype chain**
```javascript
// ✅ Yêu cầu: Thêm method vào prototype
function Person(name) {
  this.name = name;
}

// 📝 Code của bạn:
// Thêm greet method vào Person.prototype


// ✅ Test:
const alice = new Person("Alice");
console.log(alice.greet()); // "Hi, I'm Alice"
```

---

### 3.4 Async JavaScript

**Bài 32: Promise cơ bản**
```javascript
// ✅ Yêu cầu: Tạo promise resolve sau 1 giây
function waitOneSecond() {
  // 📝 Code của bạn:

}

waitOneSecond().then(() => {
  console.log("1 second passed!");
});
```

**Bài 33: Async/await error handling**
```javascript
// ✅ Yêu cầu: Viết function fetch với error handling
async function fetchData(url) {
  // 📝 Code của bạn:

}

// ✅ Test:
fetchData("/api/users");
```

**Bài 34: Promise.all**
```javascript
// ✅ Yêu cầu: Fetch nhiều endpoints song song
async function fetchAllData() {
  // 📝 Code của bạn:

}

// ✅ Test:
const [users, posts, comments] = await fetchAllData();
```

**Bài 35: Retry failed request**
```javascript
// ✅ Yêu cầu: Retry failed promise max 3 lần
async function fetchWithRetry(url, maxRetries = 3) {
  // 📝 Code của bạn:

}

// ✅ Test:
fetchWithRetry("/api/flaky-endpoint");
```

---

### 3.5 Event Loop

**Bài 36: Predict output**
```javascript
// ✅ Yêu cầu: Dự đoán output và giải thích
console.log("1");

setTimeout(() => console.log("2"), 0);

Promise.resolve().then(() => console.log("3"));

console.log("4");

// Output là gì? Giải thích?
```

**Bài 37: Microtask scheduling**
```javascript
// ✅ Yêu cầu: Dự đoán output
Promise.resolve().then(() => {
  console.log("A");
  Promise.resolve().then(() => console.log("B"));
});
setTimeout(() => console.log("C"), 0);
console.log("D");

// Output?
```

---

## Level 4: Expert

### 4.1 Functional Programming

**Bài 38: Implement map**
```javascript
// ✅ Yêu cầu: Tự implement Array.prototype.map
Array.prototype.myMap = function(callback) {
  // 📝 Code của bạn:

};

// ✅ Test:
const result = [1, 2, 3].myMap(x => x * 2);
console.log(result); // [2, 4, 6]
```

**Bài 39: Implement reduce**
```javascript
// ✅ Yêu cầu: Tự implement Array.prototype.reduce
Array.prototype.myReduce = function(callback, initialValue) {
  // 📝 Code của bạn:

};

// ✅ Test:
const sum = [1, 2, 3, 4].myReduce((acc, x) => acc + x, 0);
console.log(sum); // 10
```

**Bài 40: Compose functions**
```javascript
// ✅ Yêu cầu: Implement function compose
function compose(...functions) {
  // 📝 Code của bạn:

}

// ✅ Test:
const add2 = x => x + 2;
const multiply3 = x => x * 3;
const composed = compose(multiply3, add2);
console.log(composed(5)); // 21 (5 + 2 = 7, 7 * 3 = 21)
```

---

### 4.2 Design Patterns

**Bài 41: Singleton pattern**
```javascript
// ✅ Yêu cầu: Implement singleton
class Database {
  // 📝 Code của bạn:

}

// ✅ Test:
const db1 = new Database();
const db2 = new Database();
console.log(db1 === db2); // true (cùng instance)
```

**Bài 42: Module pattern**
```javascript
// ✅ Yêu cầu: Tạo module với private variables
const ShoppingCart = (function() {
  // 📝 Code của bạn:

})();

// ✅ Test:
ShoppingCart.addItem({ id: 1, price: 10 });
ShoppingCart.addItem({ id: 2, price: 20 });
console.log(ShoppingCart.getTotal()); // 30
```

---

### 4.3 Performance & Optimization

**Bài 43: Debounce function**
```javascript
// ✅ Yêu cầu: Implement debounce
function debounce(func, delay) {
  // 📝 Code của bạn:

}

// ✅ Test:
const search = debounce((query) => {
  console.log("Searching:", query);
}, 300);

search("a"); // Cancelled
search("ab"); // Cancelled
search("abc"); // Executed after 300ms
```

**Bài 44: Throttle function**
```javascript
// ✅ Yêu cầu: Implement throttle
function throttle(func, limit) {
  // 📝 Code của bạn:

}

// ✅ Test:
const scrollHandler = throttle(() => {
  console.log("Scrolling...");
}, 100);

window.addEventListener("scroll", scrollHandler);
```

**Bài 45: Memoization**
```javascript
// ✅ Yêu cầu: Implement memoize
function memoize(fn) {
  // 📝 Code của bạn:

}

// ✅ Test:
const factorial = memoize(function(n) {
  if (n <= 1) return 1;
  return n * this(n - 1);
});

console.log(factorial(5)); // 120
console.log(factorial(5)); // Cached!
```

---

## Project Challenges

### 🟢 Beginner Projects

**Project 1: To-Do List**
```
Yêu cầu:
- Thêm task mới
- Mark task hoàn thành
- Xóa task
- Lưu vào localStorage
- Filter: All / Active / Completed
```

**Project 2: Calculator**
```
Yêu cầu:
- Các phép tính cơ bản: +, -, *, /
- Xử lý decimal
- History calculations
- Keyboard support
```

**Project 3: Digital Clock**
```
Yêu cầu:
- Hiển thị giờ hiện tại
- Format: HH:MM:SS
- Toggle 12h/24h
- Stopwatch feature
```

---

### 🟡 Intermediate Projects

**Project 4: Weather App**
```
Yêu cầu:
- Fetch từ OpenWeatherMap API
- Hiển thị nhiệt độ, độ ẩm, wind speed
- Search city
- 5-day forecast
```

**Project 5: Movie Search**
```
Yêu cầu:
- Fetch từ OMDb API
- Search movies
- Display poster, rating, plot
- Add to favorites (localStorage)
```

**Project 6: Expense Tracker**
```
Yêu cầu:
- Add income/expense
- Category selection
- Chart visualization
- Filter by date range
- Export to CSV
```

---

### 🟠 Advanced Projects

**Project 7: Real-time Chat**
```
Yêu cầu:
- WebSocket connection
- Multiple rooms
- User authentication
- Message history
- Typing indicators
```

**Project 8: E-commerce Cart**
```
Yêu cầu:
- Product listing
- Add/remove from cart
- Quantity update
- Checkout flow
- Payment integration (Stripe)
- Order history
```

**Project 9: Task Management (Trello clone)**
```
Yêu cầu:
- Drag & drop tasks
- Multiple boards
- Task assignments
- Due dates
- Labels & filters
- Real-time updates
```

---

## Solutions

<details>
<summary><strong>Bài 6: checkEvenOdd</strong></summary>

```javascript
function checkEvenOdd(num) {
  return num % 2 === 0 ? "Even" : "Odd";
}
```
</details>

<details>
<summary><strong>Bài 7: gradeStudent</strong></summary>

```javascript
function gradeStudent(score) {
  if (score >= 90) return "Excellent";
  if (score >= 80) return "Good";
  if (score >= 70) return "Fair";
  if (score >= 60) return "Pass";
  return "Fail";
}
```
</details>

<details>
<summary><strong>Bài 10: isPrime</strong></summary>

```javascript
function isPrime(num) {
  if (num <= 1) return false;
  if (num <= 3) return true;
  if (num % 2 === 0 || num % 3 === 0) return false;

  for (let i = 5; i * i <= num; i += 6) {
    if (num % i === 0 || num % (i + 2) === 0) return false;
  }
  return true;
}
```
</details>

<details>
<summary><strong>Bài 15: Array methods</strong></summary>

```javascript
const evenNumbers = numbers.filter(n => n % 2 === 0);
const doubled = numbers.map(n => n * 2);
const total = numbers.reduce((acc, n) => acc + n, 0);
const firstGreaterThanFive = numbers.find(n => n > 5);
```
</details>

<details>
<summary><strong>Bài 17: unique</strong></summary>

```javascript
function unique(arr) {
  return [...new Set(arr)];
}
```
</details>

<details>
<summary><strong>Bài 26: createCounter</strong></summary>

```javascript
function createCounter() {
  let count = 0;
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count
  };
}
```
</details>

<details>
<summary><strong>Bài 32: waitOneSecond</strong></summary>

```javascript
function waitOneSecond() {
  return new Promise(resolve => setTimeout(resolve, 1000));
}
```
</details>

<details>
<summary><strong>Bài 36: Event Loop output</strong></summary>

```javascript
// Output: 1, 4, 3, 2
// Giải thích:
// 1. "1" - đồng bộ
// 4. "4" - đồng bộ
// 3. "3" - microtask (Promise.then)
// 2. "2" - macrotask (setTimeout)
```
</details>

<details>
<summary><strong>Bài 38: myMap</strong></summary>

```javascript
Array.prototype.myMap = function(callback) {
  const result = [];
  for (let i = 0; i < this.length; i++) {
    result.push(callback(this[i], i, this));
  }
  return result;
};
```
</details>

<details>
<summary><strong>Bài 43: debounce</strong></summary>

```javascript
function debounce(func, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}
```
</details>

<details>
<summary><strong>Bài 45: memoize</strong></summary>

```javascript
function memoize(fn) {
  const cache = {};
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache[key]) return cache[key];
    const result = fn.apply(this, args);
    cache[key] = result;
    return result;
  };
}
```
</details>

---

## 📚 Resources

- [Codewars](https://www.codewars.com/) - Coding challenges
- [Exercism](https://exercism.io/tracks/javascript) - Mentored exercises
- [LeetCode](https://leetcode.com/) - Interview prep
- [JavaScript30](https://javascript30.com/) - 30 vanilla JS projects
