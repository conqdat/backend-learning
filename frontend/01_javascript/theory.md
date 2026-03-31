# JavaScript Theory: Complete Guide

> Từ Zero đến Hero - Học vững JavaScript trước khi đụng framework

---

## 📑 Mục lục

1. [Nhập môn](#1-nhập-môn)
2. [Biến & Hằng số](#2-biến--hằng-số)
3. [Kiểu dữ liệu](#3-kiểu-dữ-liệu)
4. [Toán tử](#4-toán-tử)
5. [Điều kiện & Rẽ nhánh](#5-điều-kiện--rẽ-nhánh)
6. [Vòng lặp](#6-vòng-lặp)
7. [Hàm (Functions)](#7-hàm-functions)
8. [Array & Object](#8-array--object)
9. [DOM Manipulation](#9-dom-manipulation)
10. [Events](#10-events)
11. [ES6+ Features](#11-es6-features)
12. [Async JavaScript](#12-async-javascript)
13. [Modules](#13-modules)
14. [Event Loop](#14-event-loop)
15. [Advanced Concepts](#15-advanced-concepts)

---

## 1. Nhập môn

### JavaScript là gì?

JavaScript (JS) là ngôn ngữ lập trình **dynamic**, **interpreted** (hoặc JIT-compiled), hỗ trợ **multi-paradigm** (OOP, functional, imperative).

```javascript
// JavaScript chạy ở đâu?
// 1. Browser (Client-side)
console.log("Hello from browser!");

// 2. Node.js (Server-side)
// Chạy: node file.js

// 3. Runtime environments khác: Bun, Deno, Bun
```

### Cách chạy JavaScript

```bash
# 1. Trong browser console (F12)
# 2. Nhúng vào HTML
<script src="app.js"></script>

# 3. Chạy bằng Node.js
node app.js

# 4. Online playgrounds
# - CodePen, JSFiddle, CodeSandbox, Replit
```

### `console` methods

```javascript
console.log("Thông thường");      // Logging thường
console.warn("Cảnh báo!");         // Warning
console.error("Lỗi!");             // Error
console.info("Thông tin");         // Info
console.table([{name: "Alice"}, {name: "Bob"}]); // Table
console.time("timer");             // Bắt đầu timer
console.timeEnd("timer");          // Kết thúc timer
```

---

## 2. Biến & Hằng số

### `const`, `let`, `var`

```javascript
// ✅ const - Hằng số (KHÔNG thể gán lại)
const PI = 3.14159;
const USER = { name: "Alice" };
USER.name = "Bob"; // ✅ OK - mutate object
// USER = {};      // ❌ Lỗi - không thể gán lại

// ✅ let - Biến (CÓ thể gán lại, block-scoped)
let count = 0;
count = 1; // ✅ OK

// ❌ var - Legacy (function-scoped, NÊN TRÁNH)
var oldWay = "deprecated";
```

### Quy tắc đặt tên

```javascript
// ✅ Đúng
let userName = "Alice";      // camelCase - chuẩn JS
const MAX_COUNT = 100;       // UPPER_CASE - cho constants
function calculateTotal() {} // camelCase - cho functions
class UserProfile {}         // PascalCase - cho classes

// ❌ Sai
let user-name = "Alice";     // Dấu gạch ngang không được phép
let 123name = "Alice";       // Không bắt đầu bằng số
let for = "Alice";           // Từ khóa không được làm tên biến
```

### Scope (Phạm vi)

```javascript
// Block scope - let/const
{
  let blockVar = "inside";
  const BLOCK_CONST = "constant";
}
// console.log(blockVar); // ❌ ReferenceError

// Function scope - var
function test() {
  var funcVar = "inside function";
}
// console.log(funcVar); // ❌ ReferenceError

// Lexical scope - Nested functions
function outer() {
  const outerVar = "outer";
  function inner() {
    console.log(outerVar); // ✅ "outer" - inner truy cập outer
  }
  inner();
}
```

---

## 3. Kiểu dữ liệu

### 7 kiểu dữ liệu nguyên thủy (Primitives)

```javascript
// 1. String - Chuỗi
const name = "Alice";
const greeting = `Hello, ${name}!`; // Template literal

// 2. Number - Số (integer & float)
const age = 25;
const price = 99.99;
const infinity = Infinity;
const notNumber = NaN; // Not a Number

// 3. BigInt - Số nguyên lớn
const huge = 123456789012345678901234567890n;

// 4. Boolean - Đúng/Sai
const isAdult = true;
const isChild = false;

// 5. Undefined - Biến khai báo chưa gán giá trị
let notAssigned;
console.log(notAssigned); // undefined

// 6. Null - Giá trị rỗng (cố ý)
const empty = null;

// 7. Symbol - Định danh duy nhất
const id = Symbol("user-id");
const id2 = Symbol("user-id");
console.log(id === id2); // false - luôn duy nhất
```

### Reference types

```javascript
// Object - Object literal
const person = {
  name: "Alice",
  age: 25,
  sayHi: function() {
    console.log(`Hi, I'm ${this.name}`);
  }
};

// Array - Mảng
const numbers = [1, 2, 3, 4, 5];
const mixed = [1, "two", true, null, { nested: "object" }];

// Function - Hàm (cũng là object)
const add = (a, b) => a + b;

// Date, RegExp, Map, Set, WeakMap, WeakSet
const now = new Date();
const pattern = /abc/i;
const map = new Map([["key", "value"]]);
const set = new Set([1, 2, 3]);
```

### Typeof & Type coercion

```javascript
// typeof operator
typeof "hello"      // "string"
typeof 42           // "number"
typeof true         // "boolean"
typeof undefined    // "undefined"
typeof null         // "object" ⚠️ Bug lịch sử!
typeof {}           // "object"
typeof []           // "object" ⚠️ Array cũng là object!
typeof function(){} // "function"

// Type coercion - Chuyển đổi kiểu tự động
"5" + 3      // "53" - string concatenation
"5" - 3      // 2  - numeric subtraction
"5" * "2"    // 10 - numeric multiplication
true + 1     // 2
false + 1    // 1
null + 1     // 1
undefined + 1 // NaN

// Explicit conversion
Number("42")      // 42
String(42)        // "42"
Boolean("")       // false (falsy)
Boolean("hello")  // true (truthy)
```

### Falsy values (6 giá trị false)

```javascript
// Falsy - Chuyển thành false
false
0
-0
0n
""
null
undefined
NaN

// Truthy - Mọi thứ còn lại là true
"0"        // true (string không rỗng)
[]         // true (array rỗng vẫn truthy!)
{}         // true
function(){} // true
```

---

## 4. Toán tử

### Toán tử gán

```javascript
let x = 10;
x += 5;   // x = x + 5 = 15
x -= 3;   // x = x - 3 = 12
x *= 2;   // x = x * 2 = 24
x /= 4;   // x = x / 4 = 6
x %= 4;   // x = x % 4 = 2
x **= 3;  // x = x ** 3 = 8
```

### Toán tử so sánh

```javascript
5 == "5"    // true  - loose equality (type coercion)
5 === "5"   // false - strict equality (KHÔNG coercion) ✅
5 != "5"    // false
5 !== "5"   // true  ✅

10 > 5      // true
10 < 5      // false
10 >= 10    // true
10 <= 10    // true
```

### Toán tử logic

```javascript
// AND (&&) - Trả về giá trị truthy đầu tiên hoặc falsy
true && true    // true
true && false   // false
"hello" && 0    // 0 (falsy)
0 && "hello"    // 0 (short-circuit)

// OR (||) - Trả về giá trị truthy đầu tiên hoặc falsy cuối cùng
true || false   // true
false || "hi"   // "hi"
0 || "hi"       // "hi"

// Nullish coalescing (??) - Chỉ check null/undefined
const name = null ?? "Anonymous";  // "Anonymous"
const name2 = "" ?? "Anonymous";   // "" (empty string vẫn dùng)

// Optional chaining (?.) - Truy cập an toàn
const user = { profile: { name: "Alice" } };
user?.profile?.name;    // "Alice"
user?.address?.city;    // undefined (không lỗi)
```

### Toán tử bitwise

```javascript
5 & 3   // 0101 & 0011 = 0001 = 1 (AND)
5 | 3   // 0101 | 0011 = 0111 = 7 (OR)
5 ^ 3   // 0101 ^ 0011 = 0110 = 6 (XOR)
~5      // -6 (NOT)
5 << 1  // 10 (left shift = nhân 2)
5 >> 1  // 2  (right shift = chia 2)
```

---

## 5. Điều kiện & Rẽ nhánh

### if/else

```javascript
const age = 18;

if (age < 13) {
  console.log("Child");
} else if (age < 18) {
  console.log("Teen");
} else {
  console.log("Adult");
}

// Ternary operator (toán tử 3 ngôi)
const status = age >= 18 ? "Adult" : "Minor";

// Short-circuit cho side effects
isLoggedIn && showDashboard();
isAdmin || showAccessDenied();
```

### switch

```javascript
const day = "Monday";

switch (day) {
  case "Monday":
    console.log("Start of week");
    break;
  case "Friday":
    console.log("TGIF!");
    break;
  case "Saturday":
  case "Sunday":
    console.log("Weekend!");
    break;
  default:
    console.log("Weekday");
}
```

### Truthy/Falsy trong điều kiện

```javascript
const value = "";

if (value) {
  console.log("Truthy");
} else {
  console.log("Falsy"); // ✅ In ra - empty string là falsy
}

// Check tồn tại
if (user !== null && user !== undefined) {
  // ...
}
// Hoặc dùng nullish
if (user ?? false) {
  // ...
}
```

---

## 6. Vòng lặp

### for loop

```javascript
// Classic for
for (let i = 0; i < 5; i++) {
  console.log(i); // 0, 1, 2, 3, 4
}

// for...of - Iterate qua giá trị (Array, String, Map, Set)
const arr = ["a", "b", "c"];
for (const item of arr) {
  console.log(item); // "a", "b", "c"
}

// for...in - Iterate qua key (Object)
const obj = { a: 1, b: 2, c: 3 };
for (const key in obj) {
  console.log(key, obj[key]); // "a" 1, "b" 2, "c" 3
}
```

### while & do...while

```javascript
// while - Check trước, chạy sau
let i = 0;
while (i < 5) {
  console.log(i);
  i++;
}

// do...while - Chạy trước, check sau (chạy ít nhất 1 lần)
let j = 0;
do {
  console.log(j);
  j++;
} while (j < 5);
```

### break & continue

```javascript
for (let i = 0; i < 10; i++) {
  if (i === 3) continue; // Bỏ qua iteration này
  if (i === 7) break;    // Thoát vòng lặp
  console.log(i); // 0, 1, 2, 4, 5, 6
}
```

---

## 7. Hàm (Functions)

### Function Declaration

```javascript
// Function declaration - Hoisted (dùng được trước khi khai báo)
function add(a, b) {
  return a + b;
}

// Function expression - NOT hoisted
const subtract = function(a, b) {
  return a - b;
};
```

### Arrow Functions (ES6)

```javascript
// Arrow function - Ngắn gọn, lexical this
const multiply = (a, b) => {
  return a * b;
};

// Implicit return - 1 dòng không cần {}
const divide = (a, b) => a / b;

// 1 parameter - không cần ()
const square = x => x * x;

// 0 parameters - cần ()
const getRandom = () => Math.random();

// ⚠️ Arrow function KHÔNG có this riêng!
```

### Parameters & Arguments

```javascript
// Default parameters
function greet(name = "Anonymous") {
  return `Hello, ${name}!`;
}

// Rest parameters - Gom nhiều args thành array
function sum(...numbers) {
  return numbers.reduce((acc, n) => acc + n, 0);
}
sum(1, 2, 3, 4); // 10

// Spread operator - Spread array/object
const nums = [1, 2, 3];
Math.max(...nums); // 3

// Destructuring parameters
function printUser({ name, age }) {
  console.log(`${name} is ${age}`);
}

// arguments object (chỉ trong regular function)
function logArgs() {
  console.log(arguments); // Array-like object
}
```

### Return & Callbacks

```javascript
// Return value
function double(x) {
  return x * 2;
}

// Callback function - Function truyền vào function khác
function processArray(arr, callback) {
  return arr.map(callback);
}
processArray([1, 2, 3], x => x * 2); // [2, 4, 6]

// Higher-order function - Function trả về function
function multiplier(factor) {
  return function(x) {
    return x * factor;
  };
}
const double = multiplier(2);
double(5); // 10
```

---

## 8. Array & Object

### Array Methods

```javascript
const nums = [1, 2, 3, 4, 5];

// Transform
nums.map(x => x * 2);        // [2, 4, 6, 8, 10]
nums.filter(x => x > 2);     // [3, 4, 5]
nums.reduce((acc, x) => acc + x, 0); // 15

// Find
nums.find(x => x > 3);       // 4
nums.findIndex(x => x > 3);  // 3
nums.some(x => x > 4);       // true (có ít nhất 1)
nums.every(x => x > 0);      // true (tất cả)

// Iterate
nums.forEach(x => console.log(x));

// Others
nums.slice(1, 3);            // [2, 3] - không mutate
nums.splice(1, 2);           // [2, 3] - MUTATES!
nums.concat([6, 7]);         // [1,2,3,4,5,6,7]
[...nums, 6, 7];             // Modern spread syntax

// Sort
["b", "a", "c"].sort();      // ["a", "b", "c"]
[3, 1, 2].sort((a, b) => a - b); // [1, 2, 3]

// Reverse
nums.reverse();              // MUTATES!
```

### Object

```javascript
// Tạo object
const user = {
  name: "Alice",
  age: 25,
  "favorite-color": "blue", // Key có dấu gạch ngang
  1: "one",                 // Key là số
  sayHi() {                 // Method shorthand
    console.log(`Hi, I'm ${this.name}`);
  }
};

// Truy cập
user.name;                  // "Alice"
user["age"];                // 25
user["favorite-color"];     // "blue"

// Thêm/Sửa
user.email = "alice@email.com";
user.age = 26;

// Xóa
delete user.email;

// Object.keys, values, entries
Object.keys(user);          // ["name", "age", ...]
Object.values(user);        // ["Alice", 25, ...]
Object.entries(user);       // [["name", "Alice"], ["age", 25], ...]

// Object spread
const updated = { ...user, age: 26 };

// Object destructuring
const { name, age } = user;
const { name: userName } = user; // Rename
```

### Array of Objects

```javascript
const users = [
  { id: 1, name: "Alice", age: 25 },
  { id: 2, name: "Bob", age: 30 },
  { id: 3, name: "Charlie", age: 35 }
];

// Chain methods
users
  .filter(u => u.age > 25)
  .map(u => u.name)
  .join(", "); // "Bob, Charlie"

// Find by property
users.find(u => u.id === 2); // { id: 2, name: "Bob", ... }

// Group by (custom)
users.reduce((acc, user) => {
  const decade = Math.floor(user.age / 10) * 10;
  (acc[decade] = acc[decade] || []).push(user);
  return acc;
}, {});
// { 20: [{...}], 30: [{...}, {...}] }
```

---

## 9. DOM Manipulation

### Select Elements

```javascript
// Single element
document.getElementById("myId");
document.querySelector(".myClass");
document.querySelector("#myId");
document.querySelector("div.container");

// Multiple elements
document.querySelectorAll(".item"); // NodeList
document.getElementsByClassName("item"); // HTMLCollection
document.getElementsByTagName("li"); // HTMLCollection

// Traverse
element.parentElement;
element.children;
element.firstElementChild;
element.lastElementChild;
element.nextElementSibling;
element.previousElementSibling;
```

### Manipulate Elements

```javascript
// Content
element.textContent = "Plain text";
element.innerHTML = "<strong>HTML</strong>";
element.innerText = "Visible text";

// Attributes
element.getAttribute("href");
element.setAttribute("href", "https://...");
element.removeAttribute("href");
element.hasAttribute("href");

// Classes
element.classList.add("active");
element.classList.remove("active");
element.classList.toggle("active");
element.classList.contains("active");

// Styles
element.style.color = "red";
element.style.display = "none";
element.style.cssText = "color: red; display: none;";

// Create & Append
const newEl = document.createElement("div");
newEl.textContent = "New element";
parentElement.appendChild(newEl);
parentElement.insertBefore(newEl, referenceEl);

// Remove
element.remove();
parentElement.removeChild(element);
```

---

## 10. Events

### Event Listeners

```javascript
// Add listener
button.addEventListener("click", handleClick);

// Remove listener
button.removeEventListener("click", handleClick);

// Inline (không khuyến khích)
// <button onclick="handleClick()">Click</button>
```

### Event Object

```javascript
function handleClick(event) {
  event.preventDefault();  // Ngăn default action
  event.stopPropagation(); // Ngăn bubbling

  event.target;            // Element được click
  event.currentTarget;     // Element gắn listener
  event.type;              // "click"
  event.clientX, event.clientY; // Tọa độ mouse
  event.key;               // Phím nhấn (keyboard events)
}
```

### Event Bubbling & Capturing

```javascript
// Bubbling (mặc định) - Từ trong ra ngoài
// child → parent → grandparent → document

// Capturing - Từ ngoài vào trong
parent.addEventListener("click", handler, true); // capture phase

// Delegated events - Gắn listener ở parent
document.querySelector("#list").addEventListener("click", (e) => {
  if (e.target.matches(".item")) {
    console.log("Item clicked:", e.target.textContent);
  }
});
```

### Common Events

```javascript
// Mouse
"click", "dblclick", "mousedown", "mouseup", "mousemove", "mouseover", "mouseout"

// Keyboard
"keydown", "keyup", "keypress"

// Form
"submit", "change", "input", "focus", "blur"

// Document
"DOMContentLoaded", "load", "resize", "scroll"

// Drag & Drop
"dragstart", "drag", "dragend", "drop"
```

---

## 11. ES6+ Features

### let/const & Template Literals

```javascript
// Xem section 2 - Biến & Hằng số

// Template literals
const name = "Alice";
const greeting = `Hello, ${name}!`;
const multiLine = `
  Line 1
  Line 2
  Line 3
`;
```

### Destructuring

```javascript
// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
[first, second] = [second, first]; // Swap

// Object destructuring
const { name, age, email = "no@email.com" } = user;
const { name: userName } = user; // Rename

// Nested destructuring
const { user: { name } } = response;

// Function parameters
function printUser({ name, age }) {
  console.log(`${name} is ${age}`);
}
```

### Spread & Rest

```javascript
// Spread - Spread array/object
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];

const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 };

// Rest - Gom args
function sum(...nums) {
  return nums.reduce((a, b) => a + b, 0);
}

const { a, ...rest } = { a: 1, b: 2, c: 3 };
// a = 1, rest = { b: 2, c: 3 }
```

### Default Parameters

```javascript
function greet(name = "Anonymous", greeting = "Hello") {
  return `${greeting}, ${name}!`;
}
```

### Enhanced Object Literals

```javascript
const name = "Alice";
const age = 25;

const user = {
  name,           // shorthand: name: name
  age,
  sayHi() {       // method shorthand
    console.log(`Hi, I'm ${this.name}`);
  },
  ["dynamic" + "Key"]: "value" // computed property
};
```

### Classes

```javascript
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  // Method
  greet() {
    return `Hi, I'm ${this.name}`;
  }

  // Static method
  static create(name, age) {
    return new Person(name, age);
  }

  // Getter
  get info() {
    return `${this.name}, ${this.age} years old`;
  }

  // Setter
  set age(value) {
    if (value < 0) throw new Error("Age must be positive");
    this._age = value;
  }
}

// Inheritance
class Employee extends Person {
  constructor(name, age, role) {
    super(name, age);
    this.role = role;
  }

  greet() { // Override
    return `${super.greet()}, I'm a ${this.role}`;
  }
}
```

### Modules (ES6)

```javascript
// export.js
export const name = "Alice";
export function greet() { return "Hello"; }
export default class User {}

// Hoặc
const name = "Alice";
export { name };

// import.js
import User, { name, greet } from "./export.js";
import * as Everything from "./export.js";
import { default as User } from "./export.js";
```

### Promises & Async/Await

```javascript
// Promise
fetch("/api/data")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

// Async/Await
async function fetchData() {
  try {
    const response = await fetch("/api/data");
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}
```

### Optional Chaining & Nullish Coalescing

```javascript
// Optional chaining
user?.profile?.name;
users?.[0]?.name;
obj?.method?.();

// Nullish coalescing
const name = userInput ?? "Default";
```

---

## 12. Async JavaScript

### Callbacks

```javascript
// Callback pattern
function fetchData(callback) {
  setTimeout(() => {
    callback(null, "Data");
  }, 1000);
}

fetchData((err, data) => {
  if (err) console.error(err);
  else console.log(data);
});

// ⚠️ Callback hell
doSomething((result1) => {
  doSomethingElse(result1, (result2) => {
    doAnotherThing(result2, (result3) => {
      // Nested callbacks...
    });
  });
});
```

### Promises

```javascript
// Tạo Promise
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    const success = true;
    if (success) resolve("Success!");
    else reject("Failed!");
  }, 1000);
});

// Consuming Promise
promise
  .then(result => console.log(result))
  .catch(error => console.error(error))
  .finally(() => console.log("Done"));

// Promise.all - Chạy song song, tất cả phải thành công
const [user, posts] = await Promise.all([
  fetch("/api/user"),
  fetch("/api/posts")
]);

// Promise.allSettled - Chạy song song, không quan tâm success/fail
const results = await Promise.allSettled([promise1, promise2]);

// Promise.race - Cái nào xong trước lấy cái đó
const winner = await Promise.race([slowPromise, fastPromise]);

// Promise.any - Cái nào thành công đầu tiên
const firstSuccess = await Promise.any([promise1, promise2]);
```

### Async/Await

```javascript
// Async function
async function fetchData() {
  const response = await fetch("/api/data");
  const data = await response.json();
  return data;
}

// Error handling
async function fetchData() {
  try {
    const response = await fetch("/api/data");
    if (!response.ok) throw new Error("Network error");
    return await response.json();
  } catch (error) {
    console.error("Fetch failed:", error);
    throw error; // Re-throw nếu cần
  }
}

// Parallel execution
async function fetchAll() {
  const [user, posts, comments] = await Promise.all([
    fetch("/api/user"),
    fetch("/api/posts"),
    fetch("/api/comments")
  ]);
  return { user, posts, comments };
}
```

### Fetch API

```javascript
// GET request
fetch("/api/users")
  .then(res => res.json())
  .then(data => console.log(data));

// POST request
fetch("/api/users", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ name: "Alice" })
})
  .then(res => res.json())
  .then(data => console.log(data));

// With async/await
async function createUser(user) {
  const response = await fetch("/api/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user)
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return await response.json();
}
```

---

## 13. Modules

### ES6 Modules

```javascript
// math.js - Named exports
export const PI = 3.14159;
export function add(a, b) { return a + b; }

// user.js - Default export
export default class User {
  constructor(name) { this.name = name; }
}

// main.js - Imports
import User, { PI, add } from "./math.js";
import * as Math from "./math.js"; // Namespace import

// HTML
<script type="module" src="main.js"></script>
```

### CommonJS (Node.js)

```javascript
// math.js
const PI = 3.14159;
function add(a, b) { return a + b; }
module.exports = { PI, add };

// main.js
const { PI, add } = require("./math.js");
```

### Dynamic Import

```javascript
// Lazy loading
button.addEventListener("click", async () => {
  const module = await import("./heavy-module.js");
  module.doSomething();
});
```

---

## 14. Event Loop

### Call Stack, Web APIs, Callback Queue

```
┌─────────────────┐
│   Call Stack    │ ← Thực thi code đồng bộ
└─────────────────┘
        ↓
┌─────────────────┐
│  Web APIs       │ ← setTimeout, fetch, DOM events
└─────────────────┘
        ↓
┌─────────────────┐
│ Callback Queue  │ ← Chờ đến lượt
└─────────────────┘
        ↓
┌─────────────────┐
│   Event Loop    │ ← Đẩy callback vào stack khi stack rỗng
└─────────────────┘
```

### Microtasks vs Macrotasks

```javascript
console.log("1");

setTimeout(() => console.log("2"), 0); // Macrotask

Promise.resolve().then(() => console.log("3")); // Microtask

console.log("4");

// Output: 1, 4, 3, 2
// Microtasks chạy trước Macrotasks!
```

### setTimeout & setInterval

```javascript
// setTimeout - Chạy 1 lần sau X ms
const timeoutId = setTimeout(() => {
  console.log("After 1 second");
}, 1000);

clearTimeout(timeoutId); // Cancel

// setInterval - Chạy lặp lại mỗi X ms
const intervalId = setInterval(() => {
  console.log("Every second");
}, 1000);

clearInterval(intervalId); // Cancel

// Better pattern - Recursive setTimeout
function repeat() {
  // Do something
  setTimeout(repeat, 1000);
}
```

---

## 15. Advanced Concepts

### Closures

```javascript
// Closure - Function ghi nhớ lexical scope
function createCounter() {
  let count = 0; // Private variable

  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count
  };
}

const counter = createCounter();
counter.increment(); // 1
counter.increment(); // 2
counter.getCount();  // 2
// Không thể truy cập count trực tiếp!
```

### this Keyword

```javascript
// this phụ thuộc vào HOW function được gọi

// 1. Method call - this = object
const obj = {
  name: "Alice",
  greet() { console.log(this.name); }
};
obj.greet(); // "Alice"

// 2. Function call - this = undefined (strict mode) hoặc global
function standalone() { console.log(this); }
standalone(); // undefined (strict mode)

// 3. Constructor call - this = new instance
function Person(name) {
  this.name = name;
}
const p = new Person("Alice");

// 4. Arrow function - this từ lexical scope
const obj2 = {
  name: "Alice",
  greet: () => console.log(this.name) // this = window/undefined!
};

// 5. bind/call/apply
function greet(greeting) {
  console.log(`${greeting}, ${this.name}`);
}
const boundGreet = greet.bind({ name: "Alice" });
boundGreet("Hi"); // "Hi, Alice"

greet.call({ name: "Alice" }, "Hi");
greet.apply({ name: "Alice" }, ["Hi"]);
```

### Prototypes & Inheritance

```javascript
// Mọi object đều có __proto__ trỏ đến prototype
const arr = [1, 2, 3];
arr.__proto__ === Array.prototype; // true
Array.prototype.__proto__ === Object.prototype; // true

// Prototype chain
arr.toString(); // Tìm trên Array.prototype → Object.prototype

// Constructor function
function Person(name) {
  this.name = name;
}
Person.prototype.greet = function() {
  console.log(`Hi, I'm ${this.name}`);
};

// Object.create
const proto = { greet() { console.log("Hello"); } };
const obj = Object.create(proto);
```

### Generators

```javascript
// Generator function - Pause/Resume
function* numberGenerator() {
  yield 1;
  yield 2;
  yield 3;
}

const gen = numberGenerator();
gen.next(); // { value: 1, done: false }
gen.next(); // { value: 2, done: false }
gen.next(); // { value: 3, done: false }
gen.next(); // { value: undefined, done: true }

// Generator với for...of
for (const num of numberGenerator()) {
  console.log(num); // 1, 2, 3
}
```

### Proxies

```javascript
// Proxy - Intercept object operations
const handler = {
  get(target, prop) {
    console.log(`Getting ${prop}`);
    return target[prop];
  },
  set(target, prop, value) {
    console.log(`Setting ${prop} = ${value}`);
    target[prop] = value;
    return true;
  }
};

const proxy = new Proxy({ name: "Alice" }, handler);
proxy.name; // "Getting name" → "Alice"
proxy.age = 25; // "Setting age = 25"
```

### Symbols

```javascript
// Symbol - Unique identifier
const id = Symbol("id");
const id2 = Symbol("id");
id === id2; // false

const user = {
  [id]: 1,
  name: "Alice"
};
user[id]; // 1

// Well-known symbols
array[Symbol.iterator];
"hello"[Symbol.iterator];
```

### WeakMap & WeakSet

```javascript
// WeakMap - Keys có thể bị garbage collect
const weakMap = new WeakMap();
const obj = {};
weakMap.set(obj, "value");
// Khi obj không còn reference, entry tự động bị xóa

// WeakSet - Chỉ chứa objects, không iterate được
const weakSet = new WeakSet();
weakSet.add(obj);
```

### Typed Arrays

```javascript
// Binary data
const int8 = new Int8Array(8);      // -128 to 127
const uint8 = new Uint8Array(8);    // 0 to 255
const int16 = new Int16Array(4);
const float32 = new Float32Array(4);

// ArrayBuffer
const buffer = new ArrayBuffer(16);
const view = new Uint8Array(buffer);
view[0] = 255;
```

---

## 📚 Tài liệu tham khảo

- [MDN JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)
- [33 JS Concepts](https://github.com/leonardomso/33-js-concepts)
