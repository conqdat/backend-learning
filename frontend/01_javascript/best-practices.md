# JavaScript Best Practices

> Kinh nghiệm thực tế từ Senior Developers - Code sạch, an toàn, maintainable

---

## 📑 Mục lục

1. [Variables & Constants](#1-variables--constants)
2. [Functions](#2-functions)
3. [Objects & Arrays](#3-objects--arrays)
4. [Async JavaScript](#4-async-javascript)
5. [DOM Manipulation](#5-dom-manipulation)
6. [Error Handling](#6-error-handling)
7. [Security](#7-security)
8. [Performance](#8-performance)
9. [Code Organization](#9-code-organization)
10. [Debugging](#10-debugging)
11. [Anti-patterns](#11-anti-patterns)

---

## 1. Variables & Constants

### ✅ DO: Use `const` by default

```javascript
// ✅ Tốt - const cho giá trị không gán lại
const MAX_RETRIES = 3;
const config = { api: "https://api.example.com" };

// ✅ Dùng let khi cần reassign
let count = 0;
count = count + 1;

// ❌ Tránh - var (function-scoped, dễ gây bug)
var oldWay = "deprecated";
```

### ✅ DO: Use meaningful names

```javascript
// ✅ Tốt - Rõ nghĩa
const daysUntilExpiration = 30;
const isActive = true;
const getUserById = (id) => { ... };

// ❌ Tệ - Không rõ nghĩa
const d = 30;
const flag = true;
const fn = (x) => { ... };
```

### ✅ DO: Use destructuring

```javascript
// ✅ Tốt - Destructuring
const { name, age } = user;
const [first, second] = items;

// ❌ Dài dòng
const name = user.name;
const age = user.age;
const first = items[0];
const second = items[1];
```

### ✅ DO: Use template literals

```javascript
// ✅ Tốt - Template literal
const greeting = `Hello, ${name}!`;
const multiLine = `
  Line 1
  Line 2
`;

// ❌ Cũ
const greeting = "Hello, " + name + "!";
```

---

## 2. Functions

### ✅ DO: Keep functions small

```javascript
// ✅ Tốt - Mỗi hàm 1 việc
function getUser(id) {
  return db.query("SELECT * FROM users WHERE id = ?", [id]);
}

function validateUser(user) {
  return user.email && user.password;
}

function createUser(userData) {
  if (!validateUser(userData)) throw new Error("Invalid user");
  return getUser(userData.id);
}

// ❌ Tệ - Làm quá nhiều việc
function processUser(id, data, options) {
  // 100 dòng code...
  // Query database
  // Validate
  // Transform
  // Save
  // Send email
  // Log
}
```

### ✅ DO: Use arrow functions for callbacks

```javascript
// ✅ Tốt
users.map(u => u.name);
users.filter(u => u.age > 18);
users.reduce((acc, u) => acc + u.age, 0);

// ❌ Dài dòng
users.map(function(u) {
  return u.name;
});
```

### ✅ DO: Use default parameters

```javascript
// ✅ Tốt
function greet(name = "Anonymous") {
  return `Hello, ${name}!`;
}

// ❌ Cũ
function greet(name) {
  name = name || "Anonymous";
  return `Hello, ${name}!`;
}
```

### ✅ DO: Use rest parameters over arguments

```javascript
// ✅ Tốt
function sum(...numbers) {
  return numbers.reduce((a, b) => a + b, 0);
}

// ❌ Cũ
function sum() {
  return Array.from(arguments).reduce((a, b) => a + b, 0);
}
```

### ✅ DO: Early returns

```javascript
// ✅ Tốt - Early return
function getDiscount(user) {
  if (!user) return 0;
  if (!user.isMember) return 0;
  if (user.premium) return 0.2;
  return 0.1;
}

// ❌ Nested if
function getDiscount(user) {
  let discount = 0;
  if (user) {
    if (user.isMember) {
      if (user.premium) {
        discount = 0.2;
      } else {
        discount = 0.1;
      }
    }
  }
  return discount;
}
```

---

## 3. Objects & Arrays

### ✅ DO: Use object spread over Object.assign

```javascript
// ✅ Tốt
const updated = { ...user, age: 26 };

// ❌ Cũ
const updated = Object.assign({}, user, { age: 26 });
```

### ✅ DO: Use short-hand notation

```javascript
// ✅ Tốt
const name = "Alice";
const age = 25;
const user = { name, age };

// ❌ Dài dòng
const user = { name: name, age: age };
```

### ✅ DO: Use optional chaining

```javascript
// ✅ Tốt - Safe access
const city = user?.address?.city;
const name = users?.[0]?.name;

// ❌ Risky - Có thể lỗi
const city = user.address.city; // TypeError nếu user undefined
```

### ✅ DO: Use nullish coalescing for defaults

```javascript
// ✅ Tốt - Chỉ check null/undefined
const name = userInput ?? "Default";
const count = options.count ?? 0;

// ❌ OR operator - Có thể sai với falsy values
const name = userInput || "Default"; // "" sẽ thành "Default" (sai!)
```

### ✅ DO: Use array methods over loops

```javascript
// ✅ Tốt
const adults = users.filter(u => u.age >= 18);
const names = users.map(u => u.name);
const total = users.reduce((acc, u) => acc + u.age, 0);

// ❌ Imperative
const adults = [];
for (let i = 0; i < users.length; i++) {
  if (users[i].age >= 18) adults.push(users[i]);
}
```

### ✅ DO: Use destructuring in loops

```javascript
// ✅ Tốt
for (const { name, age } of users) {
  console.log(`${name} is ${age}`);
}

// ❌ Dài dòng
for (const user of users) {
  console.log(`${user.name} is ${user.age}`);
}
```

### ✅ DO: Use Set for unique values

```javascript
// ✅ Tốt
const unique = [...new Set(arr)];

// ❌ Thủ công
const unique = arr.filter((item, index) => arr.indexOf(item) === index);
```

---

## 4. Async JavaScript

### ✅ DO: Use async/await over .then()

```javascript
// ✅ Tốt - Dễ đọc
async function fetchData() {
  const response = await fetch("/api/data");
  const data = await response.json();
  return data;
}

// ❌ Chain .then()
function fetchData() {
  return fetch("/api/data")
    .then(r => r.json())
    .then(d => d);
}
```

### ✅ DO: Handle errors with try/catch

```javascript
// ✅ Tốt
async function fetchData() {
  try {
    const response = await fetch("/api/data");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Fetch failed:", error);
    throw error;
  }
}

// ❌ Không handle
async function fetchData() {
  const response = await fetch("/api/data");
  return await response.json();
}
```

### ✅ DO: Run promises in parallel

```javascript
// ✅ Tốt - Song song
const [users, posts, comments] = await Promise.all([
  fetch("/api/users"),
  fetch("/api/posts"),
  fetch("/api/comments")
]);

// ❌ Tuần tự - Chậm
const users = await fetch("/api/users");
const posts = await fetch("/api/posts");
const comments = await fetch("/api/comments");
```

### ✅ DO: Use Promise.allSettled cho non-blocking

```javascript
// ✅ Tốt - Không fail fast
const results = await Promise.allSettled([
  fetch("/api/users"),
  fetch("/api/posts"),
  fetch("/api/comments")
]);

results.forEach((result, i) => {
  if (result.status === "fulfilled") {
    console.log(`Endpoint ${i} succeeded`);
  } else {
    console.error(`Endpoint ${i} failed: ${result.reason}`);
  }
});
```

### ✅ DO: Add timeout to promises

```javascript
// ✅ Tốt - Có timeout
async function fetchWithTimeout(url, timeout = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, { signal: controller.signal });
    return await response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}
```

---

## 5. DOM Manipulation

### ✅ DO: Cache DOM references

```javascript
// ✅ Tốt
const button = document.getElementById("btn");
const output = document.getElementById("output");

button.addEventListener("click", () => {
  output.textContent = "Clicked!";
});

// ❌ Query mỗi lần
document.getElementById("btn").addEventListener("click", () => {
  document.getElementById("output").textContent = "Clicked!";
});
```

### ✅ DO: Use event delegation

```javascript
// ✅ Tốt - 1 listener cho nhiều items
document.querySelector("#list").addEventListener("click", (e) => {
  if (e.target.matches(".item")) {
    console.log("Item clicked:", e.target.textContent);
  }
});

// ❌ Nhiều listeners
document.querySelectorAll(".item").forEach(item => {
  item.addEventListener("click", handleClick);
});
```

### ✅ DO: Use classList over className

```javascript
// ✅ Tốt
element.classList.add("active");
element.classList.remove("active");
element.classList.toggle("active");

// ❌ String manipulation
element.className += " active";
element.className = element.className.replace(" active", "");
```

### ✅ DO: Use DocumentFragment cho nhiều elements

```javascript
// ✅ Tốt - 1 reflow
const fragment = document.createDocumentFragment();
items.forEach(item => {
  const li = document.createElement("li");
  li.textContent = item;
  fragment.appendChild(li);
});
list.appendChild(fragment);

// ❌ Nhiều reflows
items.forEach(item => {
  const li = document.createElement("li");
  li.textContent = item;
  list.appendChild(li); // Reflow mỗi lần!
});
```

### ✅ DO: Debounce expensive operations

```javascript
// ✅ Tốt - Debounce search
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

input.addEventListener("input", debounce((e) => {
  search(e.target.value);
}, 300));
```

---

## 6. Error Handling

### ✅ DO: Throw specific errors

```javascript
// ✅ Tốt
if (!user) throw new TypeError("User not found");
if (!authorized) throw new SecurityError("Unauthorized");
if (invalidInput) throw new ValidationError("Invalid email format");

// ❌ Chung chung
throw new Error("Something went wrong");
```

### ✅ DO: Validate inputs

```javascript
// ✅ Tốt
function createUser({ name, email }) {
  if (!name || typeof name !== "string") {
    throw new TypeError("Name is required and must be string");
  }
  if (!email || !email.includes("@")) {
    throw new TypeError("Valid email is required");
  }
  // ...
}
```

### ✅ DO: Log errors properly

```javascript
// ✅ Tốt
try {
  await fetchData();
} catch (error) {
  console.error({
    message: error.message,
    stack: error.stack,
    url: window.location.href,
    timestamp: new Date().toISOString()
  });
  // Send to error tracking service
  errorTracker.report(error);
}
```

### ✅ DO: Use custom error classes

```javascript
// ✅ Tốt
class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
  }
}

// Usage
throw new ApiError(404, "User not found");
throw new ValidationError("email", "Invalid format");
```

---

## 7. Security

### ✅ DO: Sanitize user input

```javascript
// ✅ Tốt - Escape HTML
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ❌ XSS vulnerability
element.innerHTML = userInput; // ❌ User có thể inject <script>
```

### ✅ DO: Use Content Security Policy

```html
<!-- ✅ Tốt -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'">
```

### ✅ DO: Validate API responses

```javascript
// ✅ Tốt
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();

  // Validate structure
  if (!data || typeof data.name !== "string") {
    throw new Error("Invalid API response");
  }

  return data;
}
```

### ✅ DO: Avoid eval()

```javascript
// ❌ NGUY HIỂM - Code injection
eval(userInput);

// ✅ Tốt - Dùng Function constructor an toàn hơn (nếu thực sự cần)
const fn = new Function("a", "b", "return a + b");
```

### ✅ DO: Use HTTPS only

```javascript
// ✅ Tốt - Force HTTPS
if (location.protocol !== "https:") {
  location.href = `https:${location.href.slice(location.protocol.length)}`;
}
```

---

## 8. Performance

### ✅ DO: Minimize DOM manipulation

```javascript
// ✅ Tốt - Batch updates
const fragment = document.createDocumentFragment();
items.forEach(item => {
  const li = document.createElement("li");
  li.textContent = item;
  fragment.appendChild(li);
});
list.appendChild(fragment);

// ❌ Nhiều reflows
items.forEach(item => {
  const li = document.createElement("li");
  li.textContent = item;
  list.appendChild(li);
});
```

### ✅ DO: Use event delegation

```javascript
// ✅ Tốt - 1 listener
parent.addEventListener("click", (e) => {
  if (e.target.matches(".child")) handleClick(e);
});

// ❌ Nhiều listeners
children.forEach(child => {
  child.addEventListener("click", handleClick);
});
```

### ✅ DO: Lazy load heavy resources

```javascript
// ✅ Tốt - Dynamic import
button.addEventListener("click", async () => {
  const module = await import("./heavy-module.js");
  module.doSomething();
});

// ✅ Tốt - Lazy load images
<img src="placeholder.jpg" data-src="actual.jpg" loading="lazy">
```

### ✅ DO: Use requestAnimationFrame for animations

```javascript
// ✅ Tốt
function animate() {
  // Update animation
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);

// ❌ Dùng setInterval
setInterval(animate, 16); // Không smooth bằng
```

### ✅ DO: Memoize expensive calculations

```javascript
// ✅ Tốt
function memoize(fn) {
  const cache = {};
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache[key]) return cache[key];
    const result = fn(...args);
    cache[key] = result;
    return result;
  };
}

const expensiveCalc = memoize((n) => {
  // Calculation...
});
```

---

## 9. Code Organization

### ✅ DO: Use modules

```javascript
// ✅ Tốt - Modular
// utils.js
export function formatDate(date) { ... }
export function formatCurrency(amount) { ... }

// main.js
import { formatDate, formatCurrency } from "./utils.js";
```

### ✅ DO: Group related code

```javascript
// ✅ Tốt
// services/
//   api.js
//   auth.js
//   storage.js

// components/
//   Button.js
//   Modal.js

// utils/
//   helpers.js
//   validators.js
```

### ✅ DO: Use consistent naming

```javascript
// ✅ Tốt - Consistent
function getUser() {}
function createUser() {}
function updateUser() {}
function deleteUser() {}

// ❌ Inconsistent
function getUser() {}
function userCreate() {}
function update() {}
function deleteTheUser() {}
```

### ✅ DO: Add comments for WHY, not WHAT

```javascript
// ✅ Tốt - Giải thích WHY
// Dùng debounce 300ms để tránh spam API khi user gõ nhanh
input.addEventListener("input", debounce(search, 300));

// ❌ Thừa - Giải thích WHAT
// Gán i bằng 0
let i = 0;
```

---

## 10. Debugging

### ✅ DO: Use debugger statement

```javascript
function complexCalculation(data) {
  debugger; // Pause here in DevTools
  // ...
}
```

### ✅ DO: Use console methods effectively

```javascript
// ✅ Tốt
console.table(users); // Table view
console.group("User Data"); // Grouped logs
console.time("fetch"); // Timing
console.timeEnd("fetch");
console.trace(); // Stack trace
```

### ✅ DO: Use DevTools breakpoints

```
1. Source tab → Click line number
2. Conditional breakpoints
3. DOM breakpoints
4. XHR breakpoints
```

---

## 11. Anti-patterns

### ❌ DON'T: Use var

```javascript
// ❌ Tệ
var count = 0;

// ✅ Tốt
const count = 0;
```

### ❌ DON'T: Mutate shared state

```javascript
// ❌ Tệ - Mutation
function addPrice(products, price) {
  return products.map(p => {
    p.price = price; // Mutate!
    return p;
  });
}

// ✅ Tốt - Immutable
function addPrice(products, price) {
  return products.map(p => ({ ...p, price }));
}
```

### ❌ DON'T: Ignore errors

```javascript
// ❌ Tệ
fetch("/api/data").catch(() => {});

// ✅ Tốt
fetch("/api/data").catch(error => {
  console.error("Fetch failed:", error);
  // Handle gracefully
});
```

### ❌ DON'T: Use magic numbers

```javascript
// ❌ Tệ
if (status === 200) { ... }
if (retryCount > 3) { ... }

// ✅ Tốt
const HTTP_OK = 200;
const MAX_RETRIES = 3;

if (status === HTTP_OK) { ... }
if (retryCount > MAX_RETRIES) { ... }
```

### ❌ DON'T: Deep nesting

```javascript
// ❌ Tệ
if (user) {
  if (user.profile) {
    if (user.profile.address) {
      console.log(user.profile.address.city);
    }
  }
}

// ✅ Tốt
console.log(user?.profile?.address?.city);
```

### ❌ DON'T: Callback hell

```javascript
// ❌ Tệ
doSomething((result1) => {
  doSomethingElse(result1, (result2) => {
    doAnotherThing(result2, (result3) => {
      // ...
    });
  });
});

// ✅ Tốt
async function process() {
  const result1 = await doSomething();
  const result2 = await doSomethingElse(result1);
  const result3 = await doAnotherThing(result2);
}
```

### ❌ DON'T: Compare with loose equality

```javascript
// ❌ Tệ
if (x == "5") { ... }

// ✅ Tốt
if (x === "5") { ... }
```

### ❌ DON'T: Use setTimeout without cleanup

```javascript
// ❌ Tệ - Memory leak
setInterval(() => {
  // Do something
}, 1000);

// ✅ Tốt
const intervalId = setInterval(() => {
  // Do something
}, 1000);

// Cleanup when done
clearInterval(intervalId);
```

---

## 📚 Resources

- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [MDN Best Practices](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Best_practices)
- [JavaScript Clean Code](https://github.com/ryanmcdermott/clean-code-javascript)
- [33 JS Concepts](https://github.com/leonardomso/33-js-concepts)
